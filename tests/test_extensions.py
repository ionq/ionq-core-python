"""Tests for the extension API (ClientExtension, EventHook, transport wrappers)."""

import httpx
import pytest

from ionq_core import ClientExtension, EventHook, IonQClient
from ionq_core._extensions import AsyncEventHook, AsyncHookTransport, HookTransport
from ionq_core._transport import RetryTransport


class RecordingHook:
    """Sync EventHook that records calls for assertions."""

    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.responses: list[tuple[httpx.Request, httpx.Response]] = []

    def on_request(self, request: httpx.Request) -> None:
        self.requests.append(request)

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        self.responses.append((request, response))


class AsyncRecordingHook:
    """Async EventHook that records calls for assertions."""

    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.responses: list[tuple[httpx.Request, httpx.Response]] = []

    async def on_request(self, request: httpx.Request) -> None:
        self.requests.append(request)

    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        self.responses.append((request, response))


class TestClientExtensionDefaults:
    def test_default_values(self):
        ext = ClientExtension()
        assert ext.user_agent_token is None
        assert ext.default_headers == {}
        assert ext.event_hooks == ()
        assert ext.async_event_hooks == ()
        assert ext.max_retries is None
        assert ext.timeout is None
        assert ext.transport_wrapper is None
        assert ext.async_transport_wrapper is None

    def test_frozen(self):
        ext = ClientExtension()
        with pytest.raises(AttributeError):
            ext.user_agent_token = "something"  # type: ignore[misc]


class TestUserAgentToken:
    def test_extension_user_agent_appended(self):
        ext = ClientExtension(user_agent_token="qiskit-ionq/1.1.0")
        client = IonQClient(api_key="key", extension=ext)
        ua = client.get_httpx_client().headers["User-Agent"]
        assert "qiskit-ionq/1.1.0" in ua
        assert ua.startswith("ionq-core-python/")

    def test_additional_user_agent_and_extension_both_present(self):
        ext = ClientExtension(user_agent_token="qiskit-ionq/1.1.0")
        client = IonQClient(api_key="key", additional_user_agent="custom/2.0", extension=ext)
        ua = client.get_httpx_client().headers["User-Agent"]
        assert "custom/2.0" in ua
        assert "qiskit-ionq/1.1.0" in ua

    def test_no_extension_still_works(self):
        client = IonQClient(api_key="key")
        ua = client.get_httpx_client().headers["User-Agent"]
        assert ua.startswith("ionq-core-python/")

    def test_async_client_user_agent(self):
        ext = ClientExtension(user_agent_token="cirq-ionq/0.5.0")
        client = IonQClient(api_key="key", extension=ext)
        ua = client.get_async_httpx_client().headers["User-Agent"]
        assert "cirq-ionq/0.5.0" in ua


class TestDefaultHeaders:
    def test_headers_merged_into_sync_client(self):
        ext = ClientExtension(default_headers={"X-Qiskit-Version": "1.3.0", "X-Custom": "value"})
        client = IonQClient(api_key="key", extension=ext)
        h = client.get_httpx_client().headers
        assert h["X-Qiskit-Version"] == "1.3.0"
        assert h["X-Custom"] == "value"
        assert "Authorization" in h

    def test_headers_merged_into_async_client(self):
        ext = ClientExtension(default_headers={"X-Source": "test-sdk"})
        client = IonQClient(api_key="key", extension=ext)
        h = client.get_async_httpx_client().headers
        assert h["X-Source"] == "test-sdk"

    def test_extension_headers_do_not_clobber_auth(self):
        ext = ClientExtension(default_headers={"X-Extra": "yes"})
        client = IonQClient(api_key="key", extension=ext)
        h = client.get_httpx_client().headers
        assert h["Authorization"] == "apiKey key"


class TestTimeoutOverride:
    def test_extension_timeout_overrides_default(self):
        ext = ClientExtension(timeout=httpx.Timeout(120.0, connect=5.0))
        client = IonQClient(api_key="key", extension=ext)
        assert client.get_httpx_client().timeout.read == 120.0
        assert client.get_httpx_client().timeout.connect == 5.0

    def test_extension_timeout_overrides_explicit(self):
        ext = ClientExtension(timeout=httpx.Timeout(120.0))
        client = IonQClient(api_key="key", timeout=httpx.Timeout(30.0), extension=ext)
        assert client.get_httpx_client().timeout.read == 120.0

    def test_no_extension_timeout_uses_explicit(self):
        client = IonQClient(api_key="key", timeout=httpx.Timeout(30.0))
        assert client.get_httpx_client().timeout.read == 30.0


class TestMaxRetriesOverride:
    def test_extension_retries_override(self):
        ext = ClientExtension(max_retries=5)
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_httpx_client()._transport
        # Walk the transport chain to find RetryTransport
        retry = _find_retry_transport(transport)
        assert retry is not None
        assert retry._max_retries == 5

    def test_no_extension_retries_uses_explicit(self):
        client = IonQClient(api_key="key", max_retries=3)
        transport = client.get_httpx_client()._transport
        retry = _find_retry_transport(transport)
        assert retry is not None
        assert retry._max_retries == 3


def _find_retry_transport(transport) -> RetryTransport | None:
    """Walk the transport decorator chain to find the RetryTransport."""
    seen = set()
    while transport is not None:
        if id(transport) in seen:
            break
        seen.add(id(transport))
        if isinstance(transport, RetryTransport):
            return transport
        transport = getattr(transport, "_transport", None)
    return None


class TestEventHooks:
    def test_hook_protocol_satisfied_by_recording_hook(self):
        hook = RecordingHook()
        assert isinstance(hook, EventHook)

    def test_async_hook_protocol_satisfied(self):
        hook = AsyncRecordingHook()
        assert isinstance(hook, AsyncEventHook)

    def test_sync_hooks_wired_into_transport_chain(self):
        hook = RecordingHook()
        ext = ClientExtension(event_hooks=(hook,))
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_httpx_client()._transport
        assert isinstance(transport, HookTransport)
        assert transport._hooks == (hook,)

    def test_async_hooks_wired_into_transport_chain(self):
        hook = AsyncRecordingHook()
        ext = ClientExtension(async_event_hooks=(hook,))
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_async_httpx_client()._transport
        assert isinstance(transport, AsyncHookTransport)
        assert transport._hooks == (hook,)

    def test_no_hooks_skips_hook_transport(self):
        ext = ClientExtension()
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_httpx_client()._transport
        assert isinstance(transport, RetryTransport)


class FakeTransport(httpx.BaseTransport):
    def __init__(self, response: httpx.Response):
        self._response = response

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self._response

    def close(self):
        pass


class FakeAsyncTransport(httpx.AsyncBaseTransport):
    def __init__(self, response: httpx.Response):
        self._response = response

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return self._response

    async def aclose(self):
        pass


class TestHookTransportExecution:
    def test_hooks_called_in_order(self):
        hook1 = RecordingHook()
        hook2 = RecordingHook()
        response = httpx.Response(200)
        transport = HookTransport(FakeTransport(response), (hook1, hook2))
        request = httpx.Request("GET", "https://api.ionq.co/v0.4/backends")

        result = transport.handle_request(request)

        assert result is response
        assert len(hook1.requests) == 1
        assert len(hook2.requests) == 1
        assert hook1.requests[0] is request
        assert len(hook1.responses) == 1
        assert hook1.responses[0] == (request, response)

    def test_hook_exception_is_swallowed(self):
        class BrokenHook:
            def on_request(self, request):
                raise RuntimeError("boom")

            def on_response(self, request, response):
                raise RuntimeError("boom")

        response = httpx.Response(200)
        transport = HookTransport(FakeTransport(response), (BrokenHook(),))
        request = httpx.Request("GET", "https://api.ionq.co/v0.4/backends")

        result = transport.handle_request(request)
        assert result.status_code == 200


class TestAsyncHookTransportExecution:
    async def test_async_hooks_called(self):
        hook = AsyncRecordingHook()
        response = httpx.Response(200)
        transport = AsyncHookTransport(FakeAsyncTransport(response), (hook,))
        request = httpx.Request("GET", "https://api.ionq.co/v0.4/backends")

        result = await transport.handle_async_request(request)

        assert result is response
        assert len(hook.requests) == 1
        assert len(hook.responses) == 1

    async def test_async_hook_exception_is_swallowed(self):
        class BrokenAsyncHook:
            async def on_request(self, request):
                raise RuntimeError("boom")

            async def on_response(self, request, response):
                raise RuntimeError("boom")

        response = httpx.Response(200)
        transport = AsyncHookTransport(FakeAsyncTransport(response), (BrokenAsyncHook(),))
        request = httpx.Request("GET", "https://api.ionq.co/v0.4/backends")

        result = await transport.handle_async_request(request)
        assert result.status_code == 200


class TestTransportWrapper:
    def test_sync_wrapper_applied_outermost(self):
        marker = object()

        class MarkerTransport(httpx.BaseTransport):
            def __init__(self, inner):
                self.inner = inner
                self.marker = marker

            def handle_request(self, request):
                return self.inner.handle_request(request)

            def close(self):
                self.inner.close()

        ext = ClientExtension(transport_wrapper=lambda t: MarkerTransport(t))
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_httpx_client()._transport
        assert isinstance(transport, MarkerTransport)
        assert transport.marker is marker

    def test_async_wrapper_applied_outermost(self):
        class MarkerAsyncTransport(httpx.AsyncBaseTransport):
            def __init__(self, inner):
                self.inner = inner
                self.was_wrapped = True

            async def handle_async_request(self, request):
                return await self.inner.handle_async_request(request)

            async def aclose(self):
                await self.inner.aclose()

        ext = ClientExtension(async_transport_wrapper=lambda t: MarkerAsyncTransport(t))
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_async_httpx_client()._transport
        assert isinstance(transport, MarkerAsyncTransport)
        assert transport.was_wrapped is True


class TestAccessUnderlyingHttpxClient:
    def test_get_httpx_client_returns_httpx_client(self):
        client = IonQClient(api_key="key")
        httpx_client = client.get_httpx_client()
        assert isinstance(httpx_client, httpx.Client)

    def test_get_async_httpx_client_returns_async_client(self):
        client = IonQClient(api_key="key")
        async_client = client.get_async_httpx_client()
        assert isinstance(async_client, httpx.AsyncClient)

    def test_set_httpx_client_replaces(self):
        client = IonQClient(api_key="key")
        custom = httpx.Client(base_url="https://custom.example.com")
        client.set_httpx_client(custom)
        assert client.get_httpx_client() is custom
        custom.close()


class TestTransportChainOrder:
    """Verify the transport chain is: user_wrapper -> hooks -> retry -> httpx."""

    def test_full_chain_sync(self):
        hook = RecordingHook()

        class OuterTransport(httpx.BaseTransport):
            def __init__(self, inner):
                self.inner = inner

            def handle_request(self, request):
                return self.inner.handle_request(request)

            def close(self):
                self.inner.close()

        ext = ClientExtension(
            event_hooks=(hook,),
            transport_wrapper=lambda t: OuterTransport(t),
        )
        client = IonQClient(api_key="key", extension=ext)
        transport = client.get_httpx_client()._transport

        assert isinstance(transport, OuterTransport)
        assert isinstance(transport.inner, HookTransport)
        assert isinstance(transport.inner._transport, RetryTransport)
