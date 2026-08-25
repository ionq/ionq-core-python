# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Transport layer: retry via httpx-retries, error raising for IonQ API responses.

`ErrorRaisingTransport` converts HTTP error responses and connection failures
into structured `IonQError` exceptions; `build_transport` assembles the default
stack used by `IonQClient`. Idempotent methods are retried on status codes 429,
500, 502, 503, and 520-529 with exponential backoff (factor 0.5, jitter 0.5,
max 60s); POST is never retried because the API has no idempotency keys, so a
replay after an ambiguous 5xx could duplicate billable work.

Error handling bounds what it trusts from the server: at most
`MAX_ERROR_BODY_BYTES` decoded bytes of an error body are read, and
``Retry-After`` is clamped to `MAX_RETRY_AFTER` seconds (non-finite values are
discarded) before being exposed on `RateLimitError.retry_after`.
"""

import json
import math
import ssl

import httpx
from httpx_retries import Retry, RetryTransport

from .exceptions import APIConnectionError, APITimeoutError, raise_for_status

RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 502, 503, *range(520, 530)})
"""HTTP status codes that trigger an automatic retry."""

DEFAULT_MAX_RETRIES: int = 2
"""Default number of retry attempts for transient errors."""

MAX_RETRY_AFTER: float = 300.0
"""Cap (seconds) on the server-supplied ``Retry-After``: callers are documented
to sleep on `RateLimitError.retry_after`, so a forged header must stay bounded."""

MAX_ERROR_BODY_BYTES: int = 64 * 1024
"""Maximum decoded bytes read from an error response body."""


def _read_error_body(response: httpx.Response) -> bytes:
    """Read at most `MAX_ERROR_BODY_BYTES` decoded bytes of an error body.

    Streaming with a cap (instead of ``response.read()``) keeps a small
    compressed body from inflating without limit in client memory: httpx
    transparently applies whatever ``Content-Encoding`` the server chose.
    """
    body = bytearray()
    try:
        for chunk in response.iter_bytes():
            body += chunk
            if len(body) >= MAX_ERROR_BODY_BYTES:
                break
    finally:
        response.close()
    return bytes(body[:MAX_ERROR_BODY_BYTES])


async def _aread_error_body(response: httpx.Response) -> bytes:
    """Async variant of `_read_error_body`."""
    body = bytearray()
    try:
        async for chunk in response.aiter_bytes():
            body += chunk
            if len(body) >= MAX_ERROR_BODY_BYTES:
                break
    finally:
        await response.aclose()
    return bytes(body[:MAX_ERROR_BODY_BYTES])


def _raise_for_response(response: httpx.Response, content: bytes) -> None:
    try:
        body: dict | str | None = json.loads(content)
    except (ValueError, UnicodeDecodeError):
        # json.JSONDecodeError subclasses ValueError; UnicodeDecodeError covers
        # bodies that aren't decodable in the declared (or guessed) encoding.
        body = content.decode(response.encoding or "utf-8", errors="replace")[:500] or None
    message = (body.get("message") or body.get("error")) if isinstance(body, dict) else None
    try:
        parsed = float(response.headers["retry-after"])
    except (KeyError, ValueError):
        retry_after = None
    else:
        # float() accepts "inf" and overflow forms like "1e309"; a non-finite
        # value is garbage, not advice, so treat it as absent.
        retry_after = min(max(parsed, 0.0), MAX_RETRY_AFTER) if math.isfinite(parsed) else None
    raise_for_status(response.status_code, body, retry_after, message, request_id=response.headers.get("x-request-id"))


class ErrorRaisingTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Wraps a transport to raise structured IonQ exceptions on error responses.

    For HTTP 4xx/5xx responses, reads the response body (capped at
    `MAX_ERROR_BODY_BYTES` decoded bytes) and raises the appropriate
    `APIError` subclass. For connection and timeout errors from httpx,
    raises `APIConnectionError` or `APITimeoutError` respectively.

    This class implements both sync and async transport interfaces so a
    single instance works with both ``httpx.Client`` and ``httpx.AsyncClient``.

    Args:
        transport: Inner transport for sync requests (typically a
            ``RetryTransport``).
        async_transport: Inner transport for async requests; defaults to
            ``transport``. Separate inners let `build_transport` set TLS
            options, which live on distinct sync/async httpx transports.
    """

    def __init__(self, transport, async_transport=None) -> None:
        self._transport = transport
        self._async_transport = async_transport if async_transport is not None else transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = self._transport.handle_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        if response.status_code >= 400:
            _raise_for_response(response, _read_error_body(response))
        return response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            response = await self._async_transport.handle_async_request(request)
        except httpx.TimeoutException as exc:
            raise APITimeoutError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
        if response.status_code >= 400:
            _raise_for_response(response, await _aread_error_body(response))
        return response

    def close(self) -> None:
        self._transport.close()

    async def aclose(self) -> None:
        await self._async_transport.aclose()


def build_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
    verify: ssl.SSLContext | str | bool = True,
) -> ErrorRaisingTransport:
    """Build the default transport stack for `IonQClient`.

    Creates ``RetryTransport``s (from httpx-retries) with exponential
    backoff, wrapped by `ErrorRaisingTransport` for structured error handling.

    Args:
        max_retries: Maximum number of retry attempts. Defaults to
            `DEFAULT_MAX_RETRIES` (2).
        retryable_status_codes: HTTP status codes that trigger a retry.
            Defaults to `RETRYABLE_STATUS_CODES`.
        verify: TLS verification (``True``/``False``, a CA bundle path, or an
            ``ssl.SSLContext``) applied to the underlying transports; httpx
            ignores client-level ``verify`` when a custom transport is
            supplied, so it must be configured here to take effect.

    Returns:
        A configured `ErrorRaisingTransport` ready to be passed to an
        httpx client (sync or async).
    """
    retry = Retry(
        total=max_retries,
        backoff_factor=0.5,
        backoff_jitter=0.5,
        max_backoff_wait=60.0,
        status_forcelist=retryable_status_codes,
        # POST is deliberately not retryable: without idempotency keys, a replay
        # after an ambiguous 5xx could duplicate billable jobs.
    )
    return ErrorRaisingTransport(
        RetryTransport(transport=httpx.HTTPTransport(verify=verify), retry=retry),
        RetryTransport(transport=httpx.AsyncHTTPTransport(verify=verify), retry=retry),
    )
