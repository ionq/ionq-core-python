# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Transport layer: retry via httpx-retries, error raising for IonQ API responses.

This module provides the `ErrorRaisingTransport` that wraps httpx transports
to convert HTTP error responses and connection failures into structured
`IonQError` exceptions. The `build_transport` factory creates the default
transport stack: socket-opening httpx transports (carrying the caller's TLS
verification config) wrapped by two ``RetryTransport`` layers (from
httpx-retries) wrapped by ``ErrorRaisingTransport``.

Idempotent methods are retried on status codes 429, 500, 502, 503, and
520-529 as well as on transient network failures, with exponential backoff
(factor 0.5, jitter 0.5, max 60s). POST requests are never re-sent once the
request may have reached the server - the IonQ API's POST endpoints create
jobs and sessions, so a transparent re-send can duplicate a billable
submission - and instead retry only on `PRE_SEND_EXCEPTIONS`.
"""

import ssl

import httpx
from httpx_retries import Retry, RetryTransport

from .exceptions import APIConnectionError, APITimeoutError, raise_for_status

RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 502, 503, *range(520, 530)})
"""HTTP status codes that trigger an automatic retry (idempotent methods only)."""

DEFAULT_MAX_RETRIES: int = 2
"""Default number of retry attempts for transient errors."""

PRE_SEND_EXCEPTIONS: tuple[type[httpx.HTTPError], ...] = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.PoolTimeout,
)
"""Failures raised before any request bytes reach the server.

Retrying on these cannot duplicate a server-side effect, so they are safe
to retry even for non-idempotent methods like POST.
"""


def _raise_for_response(response: httpx.Response) -> None:
    try:
        body: dict | str | None = response.json()
    except (ValueError, UnicodeDecodeError):
        # json.JSONDecodeError subclasses ValueError; UnicodeDecodeError covers
        # bodies that aren't decodable in the declared (or guessed) encoding.
        body = (response.text or "")[:500] or None
    message = (body.get("message") or body.get("error")) if isinstance(body, dict) else None
    try:
        retry_after = max(0.0, float(response.headers["retry-after"]))
    except (KeyError, ValueError):
        retry_after = None
    raise_for_status(response.status_code, body, retry_after, message, request_id=response.headers.get("x-request-id"))


class ErrorRaisingTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Wraps a transport to raise structured IonQ exceptions on error responses.

    For HTTP 4xx/5xx responses, reads the response body and raises the
    appropriate `APIError` subclass. For connection and timeout errors from
    httpx, raises `APIConnectionError` or `APITimeoutError` respectively.

    This class implements both sync and async transport interfaces so a
    single instance works with both ``httpx.Client`` and ``httpx.AsyncClient``.

    Args:
        transport: The inner transport to wrap (typically a ``RetryTransport``).
    """

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


class DualTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Pairs a sync and an async transport behind both httpx interfaces.

    httpx ignores its ``verify`` argument when an explicit transport is
    supplied, so the transports that actually open sockets must be
    constructed with the caller's TLS configuration themselves. This class
    lets `build_transport` hand a single object to both ``httpx.Client``
    and ``httpx.AsyncClient``.

    Args:
        sync_transport: Transport used for synchronous requests.
        async_transport: Transport used for asynchronous requests.
    """

    def __init__(self, sync_transport: httpx.BaseTransport, async_transport: httpx.AsyncBaseTransport) -> None:
        self._sync_transport = sync_transport
        self._async_transport = async_transport

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self._sync_transport.handle_request(request)

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return await self._async_transport.handle_async_request(request)

    def close(self) -> None:
        self._sync_transport.close()

    async def aclose(self) -> None:
        await self._async_transport.aclose()


class NonIdempotentRetry(Retry):
    """Retry policy that never re-sends a request once a response arrived.

    A response with a status in `RETRYABLE_STATUS_CODES` (e.g. a
    load-balancer 503) can be returned after the server has already
    committed the request's side effect. Re-sending a POST at that point
    can duplicate a billable job or session, so this policy declares every
    status code non-retryable and relies on ``retry_on_exceptions``
    (`PRE_SEND_EXCEPTIONS`) to bound retries to failures where the request
    never left the client.
    """

    def is_retryable_status_code(self, status_code: int) -> bool:
        return False


def _retry_stack(
    transport: httpx.BaseTransport | httpx.AsyncBaseTransport,
    max_retries: int,
    retryable_status_codes: frozenset[int],
) -> RetryTransport:
    """Wrap ``transport`` (implementing both httpx interfaces) in the two-policy retry stack.

    ``RetryTransport`` applies its policy only to methods in
    ``allowed_methods`` and forwards everything else untouched, which gives a
    per-method split: the outer layer handles only POST and retries only
    `PRE_SEND_EXCEPTIONS`, while every other method falls through to the
    inner layer, which retries ``retryable_status_codes`` and transient
    network failures for idempotent methods.
    """
    idempotent = RetryTransport(
        transport=transport,
        retry=Retry(
            total=max_retries,
            backoff_factor=0.5,
            backoff_jitter=0.5,
            max_backoff_wait=60.0,
            status_forcelist=retryable_status_codes,
        ),
    )
    return RetryTransport(
        transport=idempotent,
        retry=NonIdempotentRetry(
            total=max_retries,
            backoff_factor=0.5,
            backoff_jitter=0.5,
            max_backoff_wait=60.0,
            allowed_methods=("POST",),
            retry_on_exceptions=PRE_SEND_EXCEPTIONS,
        ),
    )


def build_transport(
    max_retries: int = DEFAULT_MAX_RETRIES,
    retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
    verify: str | bool | ssl.SSLContext = True,
) -> ErrorRaisingTransport:
    """Build the default transport stack for `IonQClient`.

    The socket-opening httpx transports are constructed here with ``verify``
    because httpx ignores its own ``verify`` argument once a transport is
    supplied, making this the only place the caller's TLS configuration takes
    effect. They are wrapped by two ``RetryTransport`` layers (POST retries
    only on pre-send connection failures; idempotent methods also retry
    ``retryable_status_codes``) and by `ErrorRaisingTransport` for structured
    error handling.

    Args:
        max_retries: Maximum number of retry attempts. Defaults to
            `DEFAULT_MAX_RETRIES` (2).
        retryable_status_codes: HTTP status codes that trigger a retry of an
            idempotent request. Defaults to `RETRYABLE_STATUS_CODES`.
        verify: TLS verification applied to the underlying connections:
            ``True`` (default) uses the system trust store, an
            ``ssl.SSLContext`` uses the caller's context, ``False`` disables
            verification.

    Returns:
        A configured `ErrorRaisingTransport` ready to be passed to an
        httpx client.
    """
    real = DualTransport(httpx.HTTPTransport(verify=verify), httpx.AsyncHTTPTransport(verify=verify))
    return ErrorRaisingTransport(_retry_stack(real, max_retries, retryable_status_codes))
