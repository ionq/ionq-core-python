"""IonQ-specific client convenience wrapper."""

from __future__ import annotations

import os
import platform
import warnings
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

import httpx

from ._extensions import (
    AsyncHookTransport,
    ClientExtension,
    HookTransport,
    _AsyncErrorMapperTransport,
    _ErrorMapperTransport,
)
from ._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES, AsyncRetryTransport, RetryTransport
from .client import AuthenticatedClient

try:
    __version__ = _pkg_version("ionq-core")
except PackageNotFoundError:
    __version__ = "0.0.0"

_DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)
_AUTH_PREFIX = "apiKey"
_AUTH_HEADER = "Authorization"


def _build_user_agent(*tokens: str | None) -> str:
    parts = [
        f"ionq-core/{__version__}",
        f"python/{platform.python_version()}",
        f"httpx/{httpx.__version__}",
        f"os/{platform.system().lower()}",
        *filter(None, tokens),
    ]
    return " ".join(parts)


def IonQClient(
    *,
    api_key: str | None = None,
    base_url: str = "https://api.ionq.co/v0.4",
    max_retries: int | None = None,
    timeout: httpx.Timeout | None = None,
    additional_user_agent: str | None = None,
    extension: ClientExtension | None = None,
    **kwargs,
) -> AuthenticatedClient:
    """Create an authenticated IonQ API client.

    This is a factory function (not a class) that returns a configured
    ``AuthenticatedClient`` with retry transport, proper auth headers,
    and User-Agent identification.

    Precedence for configurable values: explicit caller arguments take
    priority over extension values, which take priority over defaults.

    Args:
        api_key: IonQ API key. Falls back to ``IONQ_API_KEY`` env var.
        base_url: API base URL.
        max_retries: Max retry attempts for transient errors (429, 5xx).
            Falls back to ``extension.max_retries``, then default (2).
        timeout: Request timeout.
            Falls back to ``extension.timeout``, then default (60s read, 10s connect).
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

    if not base_url.startswith("https://"):
        warnings.warn(
            f"base_url {base_url!r} does not use HTTPS. API keys will be sent in cleartext.",
            UserWarning,
            stacklevel=2,
        )

    if kwargs.get("verify_ssl") is False:
        warnings.warn(
            "verify_ssl=False disables TLS certificate verification. "
            "Your API key may be intercepted by a network attacker.",
            UserWarning,
            stacklevel=2,
        )

    def _ext(attr: str, default=None):
        """Resolve: explicit arg > extension field > default."""
        return getattr(extension, attr, None) if default is None else default

    user_agent = _build_user_agent(additional_user_agent, _ext("user_agent_token"))
    effective_timeout = timeout or _ext("timeout") or _DEFAULT_TIMEOUT
    effective_retries = max_retries if max_retries is not None else (_ext("max_retries") or DEFAULT_MAX_RETRIES)
    effective_retry_codes = _ext("retryable_status_codes") or RETRYABLE_STATUS_CODES

    headers: dict[str, str] = {}
    if extension and extension.default_headers:
        headers.update(extension.default_headers)
    headers["User-Agent"] = user_agent

    debug_hooks = _ext("debug_hooks") or False
    retry_kwargs = {"max_retries": effective_retries, "retryable_status_codes": effective_retry_codes}

    sync_transport: httpx.BaseTransport = RetryTransport(httpx.HTTPTransport(), **retry_kwargs)
    async_transport: httpx.AsyncBaseTransport = AsyncRetryTransport(httpx.AsyncHTTPTransport(), **retry_kwargs)

    if extension:
        if extension.event_hooks:
            sync_transport = HookTransport(sync_transport, extension.event_hooks, debug=debug_hooks)
        if extension.async_event_hooks:
            async_transport = AsyncHookTransport(async_transport, extension.async_event_hooks, debug=debug_hooks)
        if extension.error_mapper:
            sync_transport = _ErrorMapperTransport(sync_transport, extension.error_mapper)
            async_transport = _AsyncErrorMapperTransport(async_transport, extension.error_mapper)
        if extension.transport_wrapper:
            sync_transport = extension.transport_wrapper(sync_transport)
        if extension.async_transport_wrapper:
            async_transport = extension.async_transport_wrapper(async_transport)

    client = AuthenticatedClient(
        base_url=base_url,
        token=key,
        prefix=_AUTH_PREFIX,
        auth_header_name=_AUTH_HEADER,
        timeout=effective_timeout,
        headers=headers,
        httpx_args={"transport": sync_transport},
        **kwargs,
    )
    client.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=base_url,
            headers={**headers, _AUTH_HEADER: f"{_AUTH_PREFIX} {key}"},
            timeout=effective_timeout,
            transport=async_transport,
        )
    )
    return client
