"""IonQ-specific client convenience wrapper."""

import os
import platform
import warnings
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

import httpx

from ._extensions import ClientExtension, HookTransport, _ErrorMapperTransport
from ._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES, build_transport
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

    Args:
        api_key: IonQ API key. Falls back to ``IONQ_API_KEY`` env var.
        base_url: API base URL.
        max_retries: Max retry attempts for transient errors (429, 5xx).
        timeout: Request timeout.
        additional_user_agent: Extra token appended to User-Agent.
        extension: A :class:`ClientExtension` bundle provided by a downstream SDK.
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

    ext_ua = extension.user_agent_token if extension else None
    ext_timeout = extension.timeout if extension else None
    ext_retries = extension.max_retries if extension else None
    ext_retry_codes = extension.retryable_status_codes if extension else None
    debug_hooks = extension.debug_hooks if extension else False

    user_agent = _build_user_agent(additional_user_agent, ext_ua)
    effective_timeout = timeout or ext_timeout or _DEFAULT_TIMEOUT
    effective_retries = max_retries if max_retries is not None else (ext_retries or DEFAULT_MAX_RETRIES)
    effective_retry_codes = ext_retry_codes or RETRYABLE_STATUS_CODES

    headers: dict[str, str] = {}
    if extension and extension.default_headers:
        headers.update(extension.default_headers)
    headers["User-Agent"] = user_agent

    sync_transport = build_transport(effective_retries, effective_retry_codes)
    async_transport = build_transport(effective_retries, effective_retry_codes, async_=True)

    if extension:
        if extension.event_hooks:
            sync_transport = HookTransport(sync_transport, extension.event_hooks, debug=debug_hooks)
        if extension.async_event_hooks:
            async_transport = HookTransport(async_transport, extension.async_event_hooks, debug=debug_hooks)
        if extension.error_mapper:
            sync_transport = _ErrorMapperTransport(sync_transport, extension.error_mapper)
            async_transport = _ErrorMapperTransport(async_transport, extension.error_mapper)
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
