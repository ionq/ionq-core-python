# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""IonQ-specific client convenience wrapper.

`IonQClient` builds an `AuthenticatedClient` with the API key from the environment, a descriptive User-Agent, and
retrying sync and async transports.
"""

__all__ = ["IonQClient", "__version__"]

import os
import platform
import warnings
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

import httpx

from ._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES, build_transport
from .client import AuthenticatedClient
from .extensions import ClientExtension, HookTransport

try:
    __version__ = _pkg_version("ionq-core")
except PackageNotFoundError:
    __version__ = "0.0.0"

DEFAULT_BASE_URL = "https://api.ionq.co/v0.4"
DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)
_AUTH_PREFIX = "apiKey"
_AUTH_HEADER = "Authorization"


# PascalCase deliberately (not a class) so call sites read like construction.
def IonQClient(
    *,
    api_key: str | None = None,
    base_url: str = DEFAULT_BASE_URL,
    max_retries: int | None = None,
    timeout: httpx.Timeout | None = None,
    additional_user_agent: str | None = None,
    extension: ClientExtension | None = None,
    **kwargs,
) -> AuthenticatedClient:
    """Create an authenticated IonQ API client.

    Args:
        api_key: IonQ API key. Defaults to the ``IONQ_API_KEY`` environment variable.
        base_url: API base URL. Defaults to the IonQ production API.
        max_retries: Maximum retries for transient errors (429, 5xx). Defaults to 2. Set to 0 to disable retries.
        timeout: Request timeout. Defaults to 60 seconds with a 10-second connect timeout.
        additional_user_agent: Extra token appended to the User-Agent header.
        extension: Hooks, custom headers, transport wrappers, and error mappers from a downstream SDK.
        **kwargs: Passed through to `AuthenticatedClient`. ``verify_ssl`` (``True``/``False``, a CA bundle path, or
            an ``ssl.SSLContext``) also reaches the underlying httpx transports on both the sync and async paths.
            ``headers`` are merged beneath the extension defaults and the generated ``User-Agent``; ``cookies`` reach
            both the sync and async clients. ``httpx_args`` is reserved: `IonQClient` owns the transport slot.

    Returns:
        An `AuthenticatedClient` ready for both sync and async API calls.

    Raises:
        ValueError: If no API key is provided and ``IONQ_API_KEY`` is not set.

    Examples:
        ```python
        from ionq_core import IonQClient
        from ionq_core.api.backends import get_backends

        client = IonQClient()  # reads IONQ_API_KEY
        backends = get_backends.sync(client=client)
        ```

        The client also works as an async context manager:

        ```python
        async with IonQClient() as client:
            backends = await get_backends.asyncio(client=client)
        ```
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

    ext = extension or ClientExtension()
    ua_parts = [
        f"ionq-core/{__version__}",
        f"python/{platform.python_version()}",
        f"httpx/{httpx.__version__}",
        f"os/{platform.system().lower()}",
        *filter(None, (additional_user_agent, ext.user_agent_token)),
    ]
    user_agent = " ".join(ua_parts)
    effective_timeout = timeout or ext.timeout or DEFAULT_TIMEOUT
    effective_retries = next(v for v in (max_retries, ext.max_retries, DEFAULT_MAX_RETRIES) if v is not None)

    # Caller headers are merged here (extension defaults and the User-Agent win) rather than forwarded, which would
    # collide with this dict in AuthenticatedClient(**kwargs).
    headers = {**(kwargs.pop("headers", None) or {}), **ext.default_headers, "User-Agent": user_agent}

    # httpx ignores client-level `verify` when a custom transport is supplied, so verify_ssl goes into the transports.
    sync_transport = async_transport = build_transport(
        effective_retries,
        ext.retryable_status_codes or RETRYABLE_STATUS_CODES,
        verify=kwargs.get("verify_ssl", True),
    )

    if ext.event_hooks or ext.error_mapper:
        sync_transport = HookTransport(
            sync_transport,
            ext.event_hooks,
            debug=ext.debug_hooks,
            error_mapper=ext.error_mapper,
        )
    if ext.async_event_hooks or ext.error_mapper:
        async_transport = HookTransport(
            async_transport,
            ext.async_event_hooks,
            debug=ext.debug_hooks,
            error_mapper=ext.error_mapper,
        )
    if ext.transport_wrapper:
        sync_transport = ext.transport_wrapper(sync_transport)
    if ext.async_transport_wrapper:
        async_transport = ext.async_transport_wrapper(async_transport)

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
    # `set_async_httpx_client` bypasses `AuthenticatedClient`'s lazy auth-header injection, so `Authorization` is
    # merged in manually; TLS rides on `async_transport`. `_follow_redirects` is private but is the only way to mirror
    # the caller's choice here; do not add a public accessor in the hand-written layer.
    client.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=base_url,
            headers={**headers, _AUTH_HEADER: f"{_AUTH_PREFIX} {key}"},
            cookies=kwargs.get("cookies") or {},
            timeout=effective_timeout,
            transport=async_transport,
            follow_redirects=client._follow_redirects,
        )
    )
    return client
