import httpx
import pytest

from ionq_core import IonQClient, __version__
from ionq_core._transport import AsyncRetryTransport, RetryTransport


class TestIonQClient:
    def test_creates_client_with_explicit_key(self):
        c = IonQClient(api_key="my-key")
        assert c.token == "my-key"
        assert c.prefix == "apiKey"
        assert c.auth_header_name == "Authorization"

    def test_creates_client_from_env_var(self, monkeypatch):
        monkeypatch.setenv("IONQ_API_KEY", "env-key")
        assert IonQClient().token == "env-key"

    def test_explicit_key_takes_precedence_over_env(self, monkeypatch):
        monkeypatch.setenv("IONQ_API_KEY", "env-key")
        assert IonQClient(api_key="explicit-key").token == "explicit-key"

    def test_raises_without_key(self, monkeypatch):
        monkeypatch.delenv("IONQ_API_KEY", raising=False)
        with pytest.raises(ValueError, match="api_key or IONQ_API_KEY"):
            IonQClient()

    def test_default_base_url(self):
        assert IonQClient(api_key="key")._base_url == "https://api.ionq.co/v0.4"

    def test_custom_base_url(self):
        assert IonQClient(api_key="key", base_url="https://staging.ionq.co/v0.4")._base_url == (
            "https://staging.ionq.co/v0.4"
        )

    def test_auth_header_set_correctly(self):
        assert IonQClient(api_key="my-key").get_httpx_client().headers["Authorization"] == "apiKey my-key"

    def test_context_manager(self):
        with IonQClient(api_key="key") as c:
            assert c.token == "key"

    def test_user_agent_header(self):
        ua = IonQClient(api_key="key").get_httpx_client().headers["User-Agent"]
        assert ua.startswith("ionq-core-python/")
        for token in ("python/", "httpx/", "os/"):
            assert token in ua

    def test_additional_user_agent(self):
        ua = IonQClient(api_key="key", additional_user_agent="qiskit-ionq/1.0").get_httpx_client().headers["User-Agent"]
        assert "qiskit-ionq/1.0" in ua

    def test_default_timeout(self):
        t = IonQClient(api_key="key").get_httpx_client().timeout
        assert t.connect == 10.0
        assert t.read == 60.0

    def test_custom_timeout(self):
        assert IonQClient(api_key="key", timeout=httpx.Timeout(120.0)).get_httpx_client().timeout.read == 120.0

    def test_retry_transport_wired(self):
        assert isinstance(IonQClient(api_key="key").get_httpx_client()._transport, RetryTransport)

    def test_max_retries_configurable(self):
        assert IonQClient(api_key="key", max_retries=5).get_httpx_client()._transport._max_retries == 5

    def test_async_client_wired(self):
        ac = IonQClient(api_key="key").get_async_httpx_client()
        assert isinstance(ac._transport, AsyncRetryTransport)
        assert "apiKey key" in ac.headers["Authorization"]
        assert ac.headers["User-Agent"].startswith("ionq-core-python/")

    def test_version_exposed(self):
        assert isinstance(__version__, str)
        assert __version__ != ""
