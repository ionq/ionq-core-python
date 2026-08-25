# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Extension API for downstream SDKs building on ionq-core.

This module provides the `ClientExtension` configuration bundle and the
`EventHook` / `AsyncEventHook` protocols that allow downstream SDKs to
customize client behavior without modifying this library. Extensions are
passed to `IonQClient` via the ``extension`` parameter.

Example:
    ```python
    from ionq_core import IonQClient, ClientExtension, EventHook
    import httpx


    class LoggingHook(EventHook):
        def on_request(self, request: httpx.Request) -> None:
            print(f"--> {request.method} {request.url}")

        def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
            print(f"<-- {response.status_code}")


    ext = ClientExtension(
        user_agent_token="my-sdk/1.0",
        event_hooks=(LoggingHook(),),
        max_retries=5,
    )
    client = IonQClient(extension=ext)
    ```
"""

__all__ = ["AsyncEventHook", "ClientExtension", "EventHook"]

import logging
from collections.abc import Callable
from typing import Protocol, runtime_checkable

import attrs
import httpx

logger = logging.getLogger("ionq_core")


@runtime_checkable
class EventHook(Protocol):
    """Protocol for observing HTTP requests and responses (sync).

    Implement this protocol and pass instances via
    `ClientExtension.event_hooks` to receive callbacks on every request.

    Hooks may also define an optional ``on_error(request, exc)`` method,
    fired before a transport exception is re-raised. It is looked up by name
    and deliberately not part of this protocol, so minimal hooks still pass
    ``isinstance`` checks.

    Hook exceptions are logged and suppressed by default. Set
    ``debug_hooks=True`` on `ClientExtension` to re-raise them instead.
    """

    def on_request(self, request: httpx.Request) -> None:
        """Called after the request is built but before it is sent.

        Args:
            request: The outgoing HTTP request.
        """
        ...

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        """Called after a successful response is received.

        Not called for error responses: the wrapped transport raises an
        `IonQError` before this hook fires. Define ``on_error`` to observe
        failures.

        Args:
            request: The original HTTP request.
            response: The HTTP response.
        """
        ...


@runtime_checkable
class AsyncEventHook(Protocol):
    """Async counterpart of `EventHook` for the async client path.

    Implement this protocol and pass instances via
    `ClientExtension.async_event_hooks`.
    """

    async def on_request(self, request: httpx.Request) -> None:
        """Async counterpart of `EventHook.on_request`."""
        ...

    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        """Async counterpart of `EventHook.on_response`."""
        ...


@attrs.frozen
class ClientExtension:
    """Declarative configuration bundle for downstream SDK integration.

    All fields are optional. Pass an instance to `IonQClient` via the
    ``extension`` parameter to customize client behavior.

    Attributes:
        user_agent_token: Extra token appended to the ``User-Agent`` header
            (e.g. ``"my-sdk/1.0"``).
        default_headers: Headers merged into every request.
        event_hooks: Sync `EventHook` instances invoked on every request.
        async_event_hooks: Async `AsyncEventHook` instances invoked on
            every async request.
        retryable_status_codes: HTTP status codes that should trigger a retry,
            overriding ``ionq_core._transport.RETRYABLE_STATUS_CODES``.
        max_retries: Maximum retry attempts. Overrides the default of 2.
        timeout: Request timeout. Overrides the default of 60 seconds.
        transport_wrapper: Callable that wraps the sync transport, useful for
            adding middleware (e.g. caching, tracing).
        async_transport_wrapper: Callable that wraps the async transport.
        error_mapper: Callable that maps exceptions raised by the transport
            to downstream-specific exception types. Return the original
            exception to leave it unchanged.
        debug_hooks: If ``True``, hook exceptions are re-raised instead of
            being logged and suppressed. Useful during development.
    """

    user_agent_token: str | None = None
    default_headers: dict[str, str] = attrs.Factory(dict)
    event_hooks: tuple[EventHook, ...] = ()
    async_event_hooks: tuple[AsyncEventHook, ...] = ()
    retryable_status_codes: frozenset[int] | None = None
    max_retries: int | None = None
    timeout: httpx.Timeout | None = None
    transport_wrapper: Callable[[httpx.BaseTransport], httpx.BaseTransport] | None = None
    async_transport_wrapper: Callable[[httpx.AsyncBaseTransport], httpx.AsyncBaseTransport] | None = None
    error_mapper: Callable[[Exception], Exception] | None = None
    debug_hooks: bool = False


def _fire_hooks(hooks: tuple, method: str, *args, debug: bool = False) -> None:
    for hook in hooks:
        fn = getattr(hook, method, None)
        if fn is None:
            continue
        try:
            fn(*args)
        except Exception:
            if debug:
                raise
            logger.exception("%s raised; ignoring", method)


async def _afire_hooks(hooks: tuple, method: str, *args, debug: bool = False) -> None:
    for hook in hooks:
        fn = getattr(hook, method, None)
        if fn is None:
            continue
        try:
            await fn(*args)
        except Exception:
            if debug:
                raise
            logger.exception("%s raised; ignoring", method)


class HookTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Transport decorator that invokes `EventHook` instances and optionally maps exceptions.

    Wraps an inner transport, firing hook callbacks before and after each
    request. If a request raises an exception, ``on_error`` hooks are fired
    and the optional ``error_mapper`` is applied before re-raising.

    This class implements both ``httpx.BaseTransport`` and
    ``httpx.AsyncBaseTransport``, so a single instance can be used for
    both sync and async clients.

    Args:
        transport: The inner transport to wrap.
        hooks: Tuple of `EventHook` or `AsyncEventHook` instances.
        debug: If ``True``, hook exceptions are re-raised instead of
            being logged and suppressed.
        error_mapper: Optional callable that maps transport exceptions
            to custom exception types.
    """

    def __init__(
        self,
        transport,
        hooks: tuple = (),
        *,
        debug: bool = False,
        error_mapper: Callable[[Exception], Exception] | None = None,
    ) -> None:
        self._transport = transport
        self._hooks = hooks
        self._debug = debug
        self._error_mapper = error_mapper

    def _map_error(self, exc: Exception) -> None:
        if self._error_mapper is not None:
            mapped = self._error_mapper(exc)
            if mapped is not exc:
                raise mapped from exc

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        _fire_hooks(self._hooks, "on_request", request, debug=self._debug)
        try:
            response = self._transport.handle_request(request)
        except Exception as exc:
            _fire_hooks(self._hooks, "on_error", request, exc, debug=self._debug)
            self._map_error(exc)
            raise
        _fire_hooks(self._hooks, "on_response", request, response, debug=self._debug)
        return response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await _afire_hooks(self._hooks, "on_request", request, debug=self._debug)
        try:
            response = await self._transport.handle_async_request(request)
        except Exception as exc:
            await _afire_hooks(self._hooks, "on_error", request, exc, debug=self._debug)
            self._map_error(exc)
            raise
        await _afire_hooks(self._hooks, "on_response", request, response, debug=self._debug)
        return response

    def close(self) -> None:
        self._transport.close()

    async def aclose(self) -> None:
        await self._transport.aclose()
