"""IonQ-specific client convenience wrapper."""

from __future__ import annotations

import os
import platform
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

import httpx

from ._extensions import AsyncHookTransport, ClientExtension, HookTransport
from ._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES, AsyncRetryTransport, RetryTransport
from .client import AuthenticatedClient

try:
    __version__ = _pkg_version("ionq-core-python")
except PackageNotFoundError:
    __version__ = "0.0.0"

_DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def _build_user_agent(*tokens: str | None) -> str:
    """Build the User-Agent string from core info plus optional extra tokens.

    Each non-None token is appended in order.  Convention for tokens is
    ``"library-name/version"`` (e.g. ``"qiskit-ionq/1.1.0"``).
    """
    parts = [
        f"ionq-core-python/{__version__}",
        f"python/{platform.python_version()}",
        f"httpx/{httpx.__version__}",
        f"os/{platform.system().lower()}",
        *filter(None, tokens),
    ]
    return " ".join(parts)


def _build_sync_transport(
    max_retries: int,
    retryable_status_codes: frozenset[int],
    ext: ClientExtension | None,
) -> httpx.BaseTransport:
    """Assemble the sync transport chain: base -> retry -> hooks -> user wrapper."""
    transport: httpx.BaseTransport = RetryTransport(
        httpx.HTTPTransport(), max_retries=max_retries, retryable_status_codes=retryable_status_codes
    )
    if ext and ext.event_hooks:
        transport = HookTransport(transport, ext.event_hooks)
    if ext and ext.transport_wrapper:
        transport = ext.transport_wrapper(transport)
    return transport


def _build_async_transport(
    max_retries: int,
    retryable_status_codes: frozenset[int],
    ext: ClientExtension | None,
) -> httpx.AsyncBaseTransport:
    """Assemble the async transport chain: base -> retry -> hooks -> user wrapper."""
    transport: httpx.AsyncBaseTransport = AsyncRetryTransport(
        httpx.AsyncHTTPTransport(), max_retries=max_retries, retryable_status_codes=retryable_status_codes
    )
    if ext and ext.async_event_hooks:
        transport = AsyncHookTransport(transport, ext.async_event_hooks)
    if ext and ext.async_transport_wrapper:
        transport = ext.async_transport_wrapper(transport)
    return transport


def IonQClient(
    *,
    api_key: str | None = None,
    base_url: str = "https://api.ionq.co/v0.4",
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout: httpx.Timeout | None = None,
    additional_user_agent: str | None = None,
    extension: ClientExtension | None = None,
    **kwargs,
) -> AuthenticatedClient:
    """Create an authenticated IonQ API client.

    This is a factory function (not a class) that returns a configured
    ``AuthenticatedClient`` with retry transport, proper auth headers,
    and User-Agent identification.

    Args:
        api_key: IonQ API key. Falls back to ``IONQ_API_KEY`` env var.
        base_url: API base URL.
        max_retries: Max retry attempts for transient errors (429, 5xx).
            Can be overridden by ``extension.max_retries``.
        timeout: Request timeout. Default 60s read, 10s connect.
            Can be overridden by ``extension.timeout``.
        additional_user_agent: Extra token appended to User-Agent.
            Prefer ``extension.user_agent_token`` for downstream SDKs;
            both can be used simultaneously.
        extension: A :class:`ClientExtension` bundle provided by a
            downstream SDK.  See :mod:`ionq_core._extensions` for details.
        **kwargs: Passed through to :class:`AuthenticatedClient`.
    """
    key = api_key or os.environ.get("IONQ_API_KEY")
    if not key:
        raise ValueError("api_key or IONQ_API_KEY environment variable required")

    ext_ua = extension.user_agent_token if extension else None
    user_agent = _build_user_agent(additional_user_agent, ext_ua)

    effective_timeout = (
        extension.timeout if (extension and extension.timeout is not None) else (timeout or _DEFAULT_TIMEOUT)
    )
    effective_retries = extension.max_retries if (extension and extension.max_retries is not None) else max_retries
    effective_retry_codes = (
        extension.retryable_status_codes
        if (extension and extension.retryable_status_codes is not None)
        else RETRYABLE_STATUS_CODES
    )

    headers: dict[str, str] = {}
    if extension and extension.default_headers:
        headers.update(extension.default_headers)
    headers["User-Agent"] = user_agent

    sync_transport = _build_sync_transport(effective_retries, effective_retry_codes, extension)
    async_transport = _build_async_transport(effective_retries, effective_retry_codes, extension)

    client = AuthenticatedClient(
        base_url=base_url,
        token=key,
        prefix="apiKey",
        auth_header_name="Authorization",
        timeout=effective_timeout,
        headers=headers,
        httpx_args={"transport": sync_transport},
        **kwargs,
    )
    client.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=base_url,
            headers={**headers, "Authorization": f"apiKey {key}"},
            timeout=effective_timeout,
            transport=async_transport,
        )
    )
    return client
