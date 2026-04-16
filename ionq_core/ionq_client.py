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
    __version__ = _pkg_version("ionq-core")
except PackageNotFoundError:
    __version__ = "0.0.0"

_DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def _build_user_agent(*tokens: str | None) -> str:
    parts = [
        f"ionq-core/{__version__}",
        f"python/{platform.python_version()}",
        f"httpx/{httpx.__version__}",
        f"os/{platform.system().lower()}",
        *filter(None, tokens),
    ]
    return " ".join(parts)


def _ext_or(ext: ClientExtension | None, attr: str, default):
    """Return extension.attr if set, otherwise default."""
    if ext is not None:
        val = getattr(ext, attr)
        if val is not None:
            return val
    return default


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

    effective_timeout = _ext_or(extension, "timeout", timeout or _DEFAULT_TIMEOUT)
    effective_retries = _ext_or(extension, "max_retries", max_retries)
    effective_retry_codes = _ext_or(extension, "retryable_status_codes", RETRYABLE_STATUS_CODES)

    headers: dict[str, str] = {}
    if extension and extension.default_headers:
        headers.update(extension.default_headers)
    headers["User-Agent"] = user_agent

    retry_kwargs = {"max_retries": effective_retries, "retryable_status_codes": effective_retry_codes}

    sync_transport: httpx.BaseTransport = RetryTransport(httpx.HTTPTransport(), **retry_kwargs)
    if extension and extension.event_hooks:
        sync_transport = HookTransport(sync_transport, extension.event_hooks)
    if extension and extension.transport_wrapper:
        sync_transport = extension.transport_wrapper(sync_transport)

    async_transport: httpx.AsyncBaseTransport = AsyncRetryTransport(httpx.AsyncHTTPTransport(), **retry_kwargs)
    if extension and extension.async_event_hooks:
        async_transport = AsyncHookTransport(async_transport, extension.async_event_hooks)
    if extension and extension.async_transport_wrapper:
        async_transport = extension.async_transport_wrapper(async_transport)

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
