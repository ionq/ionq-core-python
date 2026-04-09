import pytest

from ionq_core import IonQClient, __version__
from ionq_core._transport import RetryTransport


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

    def test_user_agent_header(self):
        client = IonQClient(api_key="key")
        httpx_client = client.get_httpx_client()
        ua = httpx_client.headers["User-Agent"]
        assert ua.startswith("ionq-core-python/")
        assert "python/" in ua
        assert "httpx/" in ua
        assert "os/" in ua

    def test_additional_user_agent(self):
        client = IonQClient(api_key="key", additional_user_agent="qiskit-ionq/1.0")
        httpx_client = client.get_httpx_client()
        ua = httpx_client.headers["User-Agent"]
        assert "qiskit-ionq/1.0" in ua

    def test_default_timeout(self):
        client = IonQClient(api_key="key")
        httpx_client = client.get_httpx_client()
        assert httpx_client.timeout.connect == 10.0
        assert httpx_client.timeout.read == 60.0

    def test_custom_timeout(self):
        import httpx

        client = IonQClient(api_key="key", timeout=httpx.Timeout(120.0))
        httpx_client = client.get_httpx_client()
        assert httpx_client.timeout.read == 120.0

    def test_retry_transport_wired(self):
        client = IonQClient(api_key="key")
        httpx_client = client.get_httpx_client()
        assert isinstance(httpx_client._transport, RetryTransport)

    def test_max_retries_configurable(self):
        client = IonQClient(api_key="key", max_retries=5)
        httpx_client = client.get_httpx_client()
        assert httpx_client._transport._max_retries == 5

    def test_async_client_wired(self):
        from ionq_core._transport import AsyncRetryTransport

        client = IonQClient(api_key="key")
        async_client = client.get_async_httpx_client()
        assert isinstance(async_client._transport, AsyncRetryTransport)
        assert "apiKey key" in async_client.headers["Authorization"]
        assert async_client.headers["User-Agent"].startswith("ionq-core-python/")

    def test_version_exposed(self):
        assert isinstance(__version__, str)
        assert __version__ != ""
