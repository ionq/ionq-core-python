import ssl
import warnings

import httpx
import pytest

from ionq_core import AuthenticatedClient, IonQClient, __version__
from ionq_core._transport import ErrorRaisingTransport


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
        assert IonQClient(api_key="key", base_url="https://staging.example.com/v0.4")._base_url == (
            "https://staging.example.com/v0.4"
        )

    def test_auth_header_set_correctly(self):
        assert IonQClient(api_key="my-key").get_httpx_client().headers["Authorization"] == "apiKey my-key"

    def test_context_manager(self):
        with IonQClient(api_key="key") as c:
            assert c.token == "key"

    def test_user_agent_header(self):
        ua = IonQClient(api_key="key").get_httpx_client().headers["User-Agent"]
        assert ua.startswith("ionq-core/")
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

    def test_async_client_wired(self):
        ac = IonQClient(api_key="key").get_async_httpx_client()
        assert isinstance(ac._transport, ErrorRaisingTransport)
        assert "apiKey key" in ac.headers["Authorization"]
        assert ac.headers["User-Agent"].startswith("ionq-core/")

    def test_version_exposed(self):
        assert isinstance(__version__, str)
        assert __version__ != ""

    def test_token_not_in_repr(self):
        c = IonQClient(api_key="super-secret-key")
        assert "super-secret-key" not in repr(c)
        # the credential must also stay out of repr-visible state after the
        # httpx clients (and their auth headers) have been built
        c.get_httpx_client()
        c.get_async_httpx_client()
        assert "super-secret-key" not in repr(c)

    def test_caller_headers_dict_not_mutated(self):
        # A headers dict passed by the caller is caller-owned; injecting the
        # Authorization value into it would leak the key to any other client
        # sharing that dict (and into repr).
        shared = {"X-Custom": "1"}
        c = AuthenticatedClient(base_url="https://api.invalid", token="secret-token", prefix="apiKey", headers=shared)
        c.get_httpx_client()
        c.get_async_httpx_client()
        assert shared == {"X-Custom": "1"}
        assert "secret-token" not in repr(c)
        assert c.get_httpx_client().headers["Authorization"] == "apiKey secret-token"
        assert c.get_async_httpx_client().headers["Authorization"] == "apiKey secret-token"
        assert c.get_httpx_client().headers["X-Custom"] == "1"

    def test_http_base_url_warns(self):
        with pytest.warns(UserWarning, match="does not use HTTPS"):
            IonQClient(api_key="key", base_url="http://api.ionq.co/v0.4")

    def test_https_base_url_no_warning(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            IonQClient(api_key="key", base_url="https://api.ionq.co/v0.4")

    def test_verify_ssl_false_warns(self):
        with pytest.warns(UserWarning, match="verify_ssl=False"):
            IonQClient(api_key="key", verify_ssl=False)

    def test_async_client_inherits_follow_redirects(self):
        ac = IonQClient(api_key="key", follow_redirects=True).get_async_httpx_client()
        assert ac.follow_redirects is True

    def test_async_client_default_no_follow_redirects(self):
        ac = IonQClient(api_key="key").get_async_httpx_client()
        assert ac.follow_redirects is False


class TestIonQClientTls:
    """verify_ssl must reach the connection-terminating transports (CWE-295).

    httpx ignores client-level ``verify`` whenever a custom transport is
    supplied, so these tests assert on the SSL context of the innermost
    httpx transports actually used by IonQClient, on both paths.
    """

    @staticmethod
    def _ssl_contexts(c):
        sync_ctx = c.get_httpx_client()._transport._transport._sync_transport._pool._ssl_context
        async_ctx = c.get_async_httpx_client()._transport._async_transport._async_transport._pool._ssl_context
        return sync_ctx, async_ctx

    def test_default_verifies_certificates(self):
        for ctx in self._ssl_contexts(IonQClient(api_key="key")):
            assert ctx.verify_mode == ssl.CERT_REQUIRED

    def test_custom_ssl_context_reaches_both_transports(self):
        pinned = ssl.create_default_context()
        for ctx in self._ssl_contexts(IonQClient(api_key="key", verify_ssl=pinned)):
            assert ctx is pinned

    def test_verify_ssl_false_disables_verification(self):
        with pytest.warns(UserWarning, match="verify_ssl=False"):
            c = IonQClient(api_key="key", verify_ssl=False)
        for ctx in self._ssl_contexts(c):
            assert ctx.verify_mode == ssl.CERT_NONE
