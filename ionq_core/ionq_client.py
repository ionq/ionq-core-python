"""IonQ-specific client convenience wrapper."""

from __future__ import annotations

import os

from .client import AuthenticatedClient


def IonQClient(
    *,
    api_key: str | None = None,
    base_url: str = "https://api.ionq.co/v0.4",
    **kwargs,
) -> AuthenticatedClient:
    """Create an authenticated IonQ API client.

    Args:
        api_key: IonQ API key. Falls back to IONQ_API_KEY env var.
        base_url: API base URL. Defaults to production.
        **kwargs: Passed to AuthenticatedClient.
    """
    key = api_key or os.environ.get("IONQ_API_KEY")
    if not key:
        raise ValueError("api_key or IONQ_API_KEY environment variable required")
    return AuthenticatedClient(
        base_url=base_url,
        token=key,
        prefix="apiKey",
        auth_header_name="Authorization",
        **kwargs,
    )
