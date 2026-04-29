# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""IonQ-specific client convenience wrapper.

The `IonQClient` factory function is the recommended way to create an API client.
It reads the API key from the environment, configures retries with exponential
backoff, sets a descriptive User-Agent header, and wires up both the sync and
async httpx transports.
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

    This is the recommended entry point for using the library. It handles
    authentication, retry configuration, User-Agent construction, and transport
    setup for both sync and async usage.

    Args:
        api_key: IonQ API key. If not provided, reads the ``IONQ_API_KEY``
            environment variable.
        base_url: API base URL. Defaults to the IonQ production API.
        max_retries: Maximum retry attempts for transient errors (429, 5xx).
            Defaults to 2. Set to 0 to disable retries.
        timeout: Request timeout as an ``httpx.Timeout`` instance. Defaults to
            60 seconds with a 10-second connect timeout.
        additional_user_agent: Extra token appended to the User-Agent header,
            useful for identifying calling applications.
        extension: A `ClientExtension` bundle provided by a downstream SDK.
            Allows injecting hooks, custom headers, transport wrappers, and
            error mappers.
        **kwargs: Passed through to `AuthenticatedClient`.

    Returns:
        An `AuthenticatedClient` configured with retry transport and
        authentication headers, ready for both sync and async API calls.

    Raises:
        ValueError: If no API key is provided and ``IONQ_API_KEY`` is not set.

    Examples:
        Basic usage with environment variable:

        ```python
        from ionq_core import IonQClient
        from ionq_core.api.backends import get_backends

        client = IonQClient()
        backends = get_backends.sync(client=client)
        ```

        Explicit configuration:

        ```python
        import httpx
        from ionq_core import IonQClient

        client = IonQClient(
            api_key="your-api-key",
            max_retries=5,
            timeout=httpx.Timeout(30.0, connect=10.0),
        )
        ```

        Async usage with context manager:

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

    headers = {**ext.default_headers, "User-Agent": user_agent}

    sync_transport = async_transport = build_transport(
        effective_retries,
        ext.retryable_status_codes or RETRYABLE_STATUS_CODES,
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
    client.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=base_url,
            headers={**headers, _AUTH_HEADER: f"{_AUTH_PREFIX} {key}"},
            timeout=effective_timeout,
            transport=async_transport,
            verify=client._verify_ssl,
            follow_redirects=client._follow_redirects,
        )
    )
    return client
