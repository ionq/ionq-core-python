"""Extension API for downstream SDKs building on ionq-core.

Provides hooks that downstream libraries (qiskit-ionq, cirq-ionq, etc.)
use to customize client behavior without forking or monkey-patching.

Typical usage::

    from ionq_core import IonQClient, ClientExtension

    ext = ClientExtension(
        user_agent_token="qiskit-ionq/1.1.0",
        default_headers={"X-Qiskit-Version": "1.3.0"},
    )
    client = IonQClient(api_key="...", extension=ext)
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import httpx

logger = logging.getLogger("ionq_core")


@runtime_checkable
class EventHook(Protocol):
    """Protocol for observing requests and responses (sync).

    Hooks are for observation only (logging, metrics, telemetry) - they
    must not mutate the request or response.  For mutation, use a custom
    httpx transport instead.

    ``on_error`` is called when the underlying transport raises an
    exception (after retries are exhausted).  Hooks that do not implement
    ``on_error`` are silently skipped.
    """

    def on_request(self, request: httpx.Request) -> None: ...
    def on_response(self, request: httpx.Request, response: httpx.Response) -> None: ...


@runtime_checkable
class AsyncEventHook(Protocol):
    """Async counterpart of EventHook for the async client path."""

    async def on_request(self, request: httpx.Request) -> None: ...
    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None: ...


@dataclass(frozen=True, slots=True)
class ClientExtension:
    """Declarative configuration bundle for downstream SDK integration.

    All fields are optional and additive - they layer on top of the
    defaults that IonQClient already provides.

    Explicit caller arguments to ``IonQClient()`` take precedence over
    extension values, which in turn take precedence over factory defaults.
    """

    user_agent_token: str | None = None
    default_headers: dict[str, str] = field(default_factory=dict)
    event_hooks: tuple[EventHook, ...] = ()
    async_event_hooks: tuple[AsyncEventHook, ...] = ()
    retryable_status_codes: frozenset[int] | None = None
    max_retries: int | None = None
    timeout: httpx.Timeout | None = None
    transport_wrapper: Callable[[httpx.BaseTransport], httpx.BaseTransport] | None = None
    async_transport_wrapper: Callable[[httpx.AsyncBaseTransport], httpx.AsyncBaseTransport] | None = None
    error_mapper: Callable[[Exception], Exception] | None = None  # return same object to skip mapping
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


class HookTransport(httpx.BaseTransport):
    """Transport decorator that invokes EventHook instances.

    Sits between the retry transport (inner) and the user wrapper (outer).
    Hooks observe the final request/response after retries resolve.
    ``on_error`` fires when the inner transport raises.
    """

    def __init__(self, transport: httpx.BaseTransport, hooks: tuple[EventHook, ...], *, debug: bool = False) -> None:
        self._transport = transport
        self._hooks = hooks
        self._debug = debug

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        _fire_hooks(self._hooks, "on_request", request, debug=self._debug)
        try:
            response = self._transport.handle_request(request)
        except Exception as exc:
            _fire_hooks(self._hooks, "on_error", request, exc, debug=self._debug)
            raise
        _fire_hooks(self._hooks, "on_response", request, response, debug=self._debug)
        return response

    def close(self) -> None:
        self._transport.close()


class AsyncHookTransport(httpx.AsyncBaseTransport):
    """Async counterpart of HookTransport."""

    def __init__(
        self, transport: httpx.AsyncBaseTransport, hooks: tuple[AsyncEventHook, ...], *, debug: bool = False
    ) -> None:
        self._transport = transport
        self._hooks = hooks
        self._debug = debug

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await _afire_hooks(self._hooks, "on_request", request, debug=self._debug)
        try:
            response = await self._transport.handle_async_request(request)
        except Exception as exc:
            await _afire_hooks(self._hooks, "on_error", request, exc, debug=self._debug)
            raise
        await _afire_hooks(self._hooks, "on_response", request, response, debug=self._debug)
        return response

    async def aclose(self) -> None:
        await self._transport.aclose()


class _ErrorMapperTransport(httpx.BaseTransport):
    """Translates exceptions via an error_mapper callback for downstream SDKs."""

    def __init__(self, transport: httpx.BaseTransport, mapper: Callable[[Exception], Exception]) -> None:
        self._transport = transport
        self._mapper = mapper

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        try:
            return self._transport.handle_request(request)
        except Exception as exc:
            mapped = self._mapper(exc)
            if mapped is not exc:
                raise mapped from exc
            raise

    def close(self) -> None:
        self._transport.close()


class _AsyncErrorMapperTransport(httpx.AsyncBaseTransport):
    """Async counterpart of _ErrorMapperTransport."""

    def __init__(self, transport: httpx.AsyncBaseTransport, mapper: Callable[[Exception], Exception]) -> None:
        self._transport = transport
        self._mapper = mapper

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            return await self._transport.handle_async_request(request)
        except Exception as exc:
            mapped = self._mapper(exc)
            if mapped is not exc:
                raise mapped from exc
            raise

    async def aclose(self) -> None:
        await self._transport.aclose()
