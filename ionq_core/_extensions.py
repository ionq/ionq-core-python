"""Extension API for downstream SDKs building on ionq-core-python.

This module provides the hooks that downstream libraries (qiskit-ionq,
cirq-ionq, etc.) use to customize client behavior without forking or
monkey-patching.  The design is intentionally minimal: one protocol for
request/response observation, one data class for declarative configuration,
and composition through httpx's transport layer for advanced use cases.

Typical usage from a downstream SDK::

    from ionq_core import IonQClient
    from ionq_core._extensions import ClientExtension

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
    """Protocol for observing requests and responses.

    Implementations receive the httpx Request before it is sent and the
    httpx Response after it is received.  Hooks are for **observation only**
    (logging, metrics, telemetry) -- they must not mutate the request or
    response.  For mutation, use a custom httpx transport instead.

    Both methods have default no-op implementations so that concrete
    classes can override only the events they care about.
    """

    def on_request(self, request: httpx.Request) -> None:
        """Called after the request is fully prepared but before it is sent."""
        ...

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        """Called after the response is received, before it is returned to the caller."""
        ...


@runtime_checkable
class AsyncEventHook(Protocol):
    """Async counterpart of EventHook for the async client path."""

    async def on_request(self, request: httpx.Request) -> None: ...
    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None: ...


@dataclass(frozen=True, slots=True)
class ClientExtension:
    """Declarative configuration bundle for downstream SDK integration.

    All fields are optional and additive -- they layer on top of the
    defaults that IonQClient already provides.

    Attributes:
        user_agent_token: A string appended to the User-Agent header.
            Convention: ``"library-name/version"`` (e.g. ``"qiskit-ionq/1.1.0"``).
        default_headers: Extra headers merged into every request.  These are
            lower priority than per-request headers but higher priority than
            the base IonQClient headers.
        event_hooks: A sequence of EventHook instances invoked on every
            sync request/response cycle, in order.
        async_event_hooks: A sequence of AsyncEventHook instances invoked
            on every async request/response cycle, in order.
        max_retries: Override the default retry count.  ``None`` means
            use the IonQClient default.
        timeout: Override the default timeout.  ``None`` means use the
            IonQClient default.
        transport_wrapper: An optional callable that receives the
            already-configured httpx.BaseTransport (which includes retry
            logic) and returns a new transport.  This is the escape hatch
            for advanced use cases like custom caching, circuit breakers,
            or request mutation.
        async_transport_wrapper: Same as transport_wrapper but for the
            async transport.
    """

    user_agent_token: str | None = None
    default_headers: dict[str, str] = field(default_factory=dict)
    event_hooks: tuple[EventHook, ...] = ()
    async_event_hooks: tuple[AsyncEventHook, ...] = ()
    max_retries: int | None = None
    timeout: httpx.Timeout | None = None
    transport_wrapper: Callable[[httpx.BaseTransport], httpx.BaseTransport] | None = None
    async_transport_wrapper: Callable[[httpx.AsyncBaseTransport], httpx.AsyncBaseTransport] | None = None


class HookTransport(httpx.BaseTransport):
    """Transport decorator that invokes EventHook instances.

    This sits in the transport chain so that hooks fire at the same
    level as retry logic -- after retries resolve but before the
    response reaches generated API code.
    """

    def __init__(self, transport: httpx.BaseTransport, hooks: tuple[EventHook, ...]) -> None:
        self._transport = transport
        self._hooks = hooks

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        for hook in self._hooks:
            try:
                hook.on_request(request)
            except Exception:
                logger.exception("EventHook.on_request raised; ignoring")

        response = self._transport.handle_request(request)

        for hook in self._hooks:
            try:
                hook.on_response(request, response)
            except Exception:
                logger.exception("EventHook.on_response raised; ignoring")

        return response

    def close(self) -> None:
        self._transport.close()


class AsyncHookTransport(httpx.AsyncBaseTransport):
    """Async counterpart of HookTransport."""

    def __init__(self, transport: httpx.AsyncBaseTransport, hooks: tuple[AsyncEventHook, ...]) -> None:
        self._transport = transport
        self._hooks = hooks

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        for hook in self._hooks:
            try:
                await hook.on_request(request)
            except Exception:
                logger.exception("AsyncEventHook.on_request raised; ignoring")

        response = await self._transport.handle_async_request(request)

        for hook in self._hooks:
            try:
                await hook.on_response(request, response)
            except Exception:
                logger.exception("AsyncEventHook.on_response raised; ignoring")

        return response

    async def aclose(self) -> None:
        await self._transport.aclose()
