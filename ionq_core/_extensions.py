"""Extension API for downstream SDKs building on ionq-core-python.

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


class HookTransport(httpx.BaseTransport):
    """Transport decorator that invokes EventHook instances."""

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
