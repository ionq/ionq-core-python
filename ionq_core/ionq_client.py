"""IonQ-specific client convenience wrapper."""

import os
import platform
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

import httpx

from ._transport import DEFAULT_MAX_RETRIES, AsyncRetryTransport, RetryTransport
from .client import AuthenticatedClient

try:
    __version__ = _pkg_version("ionq-core-python")
except PackageNotFoundError:
    __version__ = "0.0.0"

_DEFAULT_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def _build_user_agent(additional: str | None = None) -> str:
    parts = [
        f"ionq-core-python/{__version__}",
        f"python/{platform.python_version()}",
        f"httpx/{httpx.__version__}",
        f"os/{platform.system().lower()}",
    ]
    if additional:
        parts.append(additional)
    return " ".join(parts)


def IonQClient(
    *,
    api_key: str | None = None,
    base_url: str = "https://api.ionq.co/v0.4",
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout: httpx.Timeout | None = None,
    additional_user_agent: str | None = None,
    **kwargs,
) -> AuthenticatedClient:
    """Create an authenticated IonQ API client.

    Args:
        api_key: IonQ API key. Falls back to IONQ_API_KEY env var.
        base_url: API base URL.
        max_retries: Max retry attempts for transient errors (429, 5xx).
        timeout: Request timeout. Default 60s read, 10s connect.
        additional_user_agent: Extra token appended to User-Agent.
        **kwargs: Passed to AuthenticatedClient.
    """
    key = api_key or os.environ.get("IONQ_API_KEY")
    if not key:
        raise ValueError("api_key or IONQ_API_KEY environment variable required")

    user_agent = _build_user_agent(additional_user_agent)
    timeout = timeout or _DEFAULT_TIMEOUT

    client = AuthenticatedClient(
        base_url=base_url,
        token=key,
        prefix="apiKey",
        auth_header_name="Authorization",
        timeout=timeout,
        headers={"User-Agent": user_agent},
        httpx_args={"transport": RetryTransport(httpx.HTTPTransport(), max_retries=max_retries)},
        **kwargs,
    )
    client.set_async_httpx_client(
        httpx.AsyncClient(
            base_url=base_url,
            headers={"User-Agent": user_agent, "Authorization": f"apiKey {key}"},
            timeout=timeout,
            transport=AsyncRetryTransport(httpx.AsyncHTTPTransport(), max_retries=max_retries),
        )
    )
    return client
