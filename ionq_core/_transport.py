"""Transport layer: retry via httpx-retries, error raising for IonQ API responses."""

from __future__ import annotations

from typing import Any

import httpx
from httpx_retries import Retry, RetryTransport

from ._exceptions import APIConnectionError, APITimeoutError, raise_for_status

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, *range(520, 530)})
DEFAULT_MAX_RETRIES = 2


def build_retry(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
) -> Retry:
    """Build a Retry policy matching IonQ conventions."""
    return Retry(
        total=max_retries,
        backoff_factor=0.5,
        backoff_jitter=0.5,
        max_backoff_wait=60.0,
        status_forcelist=retryable_status_codes,
        allowed_methods={"GET", "HEAD", "PUT", "DELETE", "OPTIONS"},
        respect_retry_after_header=True,
    )


def build_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
    *,
    async_: bool = False,
) -> ErrorRaisingTransport:
    """Build a transport with retry and error raising (works for both sync and async)."""
    retry = build_retry(max_retries, retryable_status_codes)
    inner_transport = httpx.AsyncHTTPTransport() if async_ else httpx.HTTPTransport()
    return ErrorRaisingTransport(RetryTransport(transport=inner_transport, retry=retry))


def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    try:
        body: dict | str | None = response.json()
    except Exception:
        text = response.text
        body = text[:500] if text else None
    message = body.get("message") or body.get("error") if isinstance(body, dict) else None
    header = response.headers.get("retry-after")
    try:
        retry_after = max(0.0, float(header)) if header is not None else None
    except ValueError:
        retry_after = None
    raise_for_status(
        response.status_code,
        body,
        retry_after,
        message,
        request_id=response.headers.get("x-request-id"),
    )


class ErrorRaisingTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Wraps a transport to raise structured IonQ exceptions on error responses."""

    def __init__(self, transport: Any) -> None:
        self._transport = transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = self._transport.handle_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        _raise_for_response(response)
        return response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = await self._transport.handle_async_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        _raise_for_response(response)
        return response

    def close(self) -> None:
        self._transport.close()

    async def aclose(self) -> None:
        await self._transport.aclose()
