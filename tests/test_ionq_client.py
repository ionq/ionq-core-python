import pytest

from ionq_core import IonQClient


class TestIonQClient:
    def test_creates_client_with_explicit_key(self):
        client = IonQClient(api_key="my-key")
        assert client.token == "my-key"
        assert client.prefix == "apiKey"
        assert client.auth_header_name == "Authorization"

    def test_creates_client_from_env_var(self, monkeypatch):
        monkeypatch.setenv("IONQ_API_KEY", "env-key")
        client = IonQClient()
        assert client.token == "env-key"

    def test_explicit_key_takes_precedence_over_env(self, monkeypatch):
        monkeypatch.setenv("IONQ_API_KEY", "env-key")
        client = IonQClient(api_key="explicit-key")
        assert client.token == "explicit-key"

    def test_raises_without_key(self, monkeypatch):
        monkeypatch.delenv("IONQ_API_KEY", raising=False)
        with pytest.raises(ValueError, match="api_key or IONQ_API_KEY"):
            IonQClient()

    def test_default_base_url(self):
        client = IonQClient(api_key="key")
        assert client._base_url == "https://api.ionq.co/v0.4"

    def test_custom_base_url(self):
        client = IonQClient(api_key="key", base_url="https://staging.ionq.co/v0.4")
        assert client._base_url == "https://staging.ionq.co/v0.4"

    def test_auth_header_set_correctly(self):
        client = IonQClient(api_key="my-key")
        httpx_client = client.get_httpx_client()
        assert httpx_client.headers["Authorization"] == "apiKey my-key"

    def test_context_manager(self):
        with IonQClient(api_key="key") as client:
            assert client.token == "key"
