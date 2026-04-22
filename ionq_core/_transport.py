"""Transport layer: retry via httpx-retries, error raising for IonQ API responses."""

from __future__ import annotations

import httpx
from httpx_retries import Retry, RetryTransport

from ._exceptions import APIConnectionError, APITimeoutError, raise_for_status

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, *range(520, 530)})
DEFAULT_MAX_RETRIES = 2
_IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})


def build_retry(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
) -> Retry:
    """Build a Retry policy matching IonQ conventions.

    POST is retried only on 429 (rate limit); idempotent methods are
    retried on all retryable status codes.  Since httpx-retries does not
    support per-status-code method filtering, we use allowed_methods for
    the broad set and rely on 429 always being retried regardless of method.
    """
    return Retry(
        total=max_retries,
        backoff_factor=0.5,
        backoff_jitter=0.5,
        max_backoff_wait=60.0,
        status_forcelist=retryable_status_codes,
        allowed_methods=_IDEMPOTENT_METHODS,
        respect_retry_after_header=True,
    )


def build_sync_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
) -> httpx.BaseTransport:
    """Build a sync transport with retry and error raising."""
    retry = build_retry(max_retries, retryable_status_codes)
    inner = RetryTransport(transport=httpx.HTTPTransport(), retry=retry)
    return ErrorRaisingTransport(inner)


def build_async_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
) -> httpx.AsyncBaseTransport:
    """Build an async transport with retry and error raising."""
    retry = build_retry(max_retries, retryable_status_codes)
    inner = RetryTransport(transport=httpx.AsyncHTTPTransport(), retry=retry)
    return AsyncErrorRaisingTransport(inner)


def _parse_error_body(response: httpx.Response) -> dict | str | None:
    try:
        return response.json()
    except Exception:
        text = response.text
        return text[:500] if text else None


def _parse_retry_after(response: httpx.Response) -> float | None:
    header = response.headers.get("retry-after")
    if header is None:
        return None
    try:
        return max(0.0, float(header))
    except ValueError:
        return None


def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    body = _parse_error_body(response)
    message = body.get("message") or body.get("error") if isinstance(body, dict) else None
    request_id = response.headers.get("x-request-id")
    raise_for_status(response.status_code, body, _parse_retry_after(response), message, request_id=request_id)


class ErrorRaisingTransport(httpx.BaseTransport):
    """Wraps a transport to raise structured IonQ exceptions on error responses."""

    def __init__(self, transport: httpx.BaseTransport) -> None:
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

    def close(self) -> None:
        self._transport.close()


class AsyncErrorRaisingTransport(httpx.AsyncBaseTransport):
    """Async counterpart of ErrorRaisingTransport."""

    def __init__(self, transport: httpx.AsyncBaseTransport) -> None:
        self._transport = transport

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = await self._transport.handle_async_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        _raise_for_response(response)
        return response

    async def aclose(self) -> None:
        await self._transport.aclose()
