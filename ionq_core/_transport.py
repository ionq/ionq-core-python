# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Transport layer: retry via httpx-retries, error raising for IonQ API responses."""

import httpx
from httpx_retries import Retry, RetryTransport

from ._exceptions import APIConnectionError, APITimeoutError, raise_for_status

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, *range(520, 530)})
DEFAULT_MAX_RETRIES = 2


def _raise_for_response(response: httpx.Response) -> None:
    try:
        body: dict | str | None = response.json()
    except Exception:
        body = (response.text or "")[:500] or None
    message = body.get("message") or body.get("error") if isinstance(body, dict) else None
    try:
        retry_after = max(0.0, float(response.headers["retry-after"]))
    except (KeyError, ValueError):
        retry_after = None
    raise_for_status(response.status_code, body, retry_after, message, request_id=response.headers.get("x-request-id"))


class ErrorRaisingTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Wraps a transport to raise structured IonQ exceptions on error responses."""

    def __init__(self, transport) -> None:
        self._transport = transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = self._transport.handle_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        if response.status_code >= 400:
            response.read()
            _raise_for_response(response)
        return response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = await self._transport.handle_async_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        if response.status_code >= 400:
            await response.aread()
            _raise_for_response(response)
        return response

    def close(self) -> None:
        self._transport.close()

    async def aclose(self) -> None:
        await self._transport.aclose()


def build_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
) -> ErrorRaisingTransport:
    return ErrorRaisingTransport(
        RetryTransport(
            retry=Retry(
                total=max_retries,
                backoff_factor=0.5,
                backoff_jitter=0.5,
                max_backoff_wait=60.0,
                status_forcelist=retryable_status_codes,
                allowed_methods=Retry.RETRYABLE_METHODS | {"POST"},
            )
        )
    )
