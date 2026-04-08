import pytest

from ionq_core import AuthenticatedClient, Client


@pytest.fixture
def client() -> Client:
    return Client(base_url="https://api.ionq.co/v0.4")


@pytest.fixture
def auth_client() -> AuthenticatedClient:
    return AuthenticatedClient(
        base_url="https://api.ionq.co/v0.4",
        token="test-api-key",
        prefix="apiKey",
        auth_header_name="Authorization",
    )
