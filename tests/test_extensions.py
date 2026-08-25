"""Tests for the extension API (ClientExtension, EventHook, transport wrappers)."""

import httpx
import pytest

from ionq_core import ClientExtension, EventHook, IonQClient
from ionq_core._transport import ErrorRaisingTransport
from ionq_core.exceptions import APIError, NotFoundError
from ionq_core.extensions import (
    AsyncEventHook,
    HookTransport,
)
from tests.conftest import BASE_URL, FakeTransport

_BACKENDS_URL = f"{BASE_URL}/backends"


class RecordingHook:
    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.responses: list[tuple[httpx.Request, httpx.Response]] = []
        self.errors: list[tuple[httpx.Request, Exception]] = []

    def on_request(self, request: httpx.Request) -> None:
        self.requests.append(request)

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        self.responses.append((request, response))

    def on_error(self, request: httpx.Request, error: Exception) -> None:
        self.errors.append((request, error))


class AsyncRecordingHook:
    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.responses: list[tuple[httpx.Request, httpx.Response]] = []
        self.errors: list[tuple[httpx.Request, Exception]] = []

    async def on_request(self, request: httpx.Request) -> None:
        self.requests.append(request)

    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        self.responses.append((request, response))

    async def on_error(self, request: httpx.Request, error: Exception) -> None:
        self.errors.append((request, error))


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
        assert ext.error_mapper is None
        assert ext.debug_hooks is False

    def test_frozen(self):
        with pytest.raises(AttributeError):
            ClientExtension().user_agent_token = "something"  # type: ignore[misc]


def _ua(client):
    return client.get_httpx_client().headers["User-Agent"]


class TestUserAgentToken:
    def test_extension_user_agent_appended(self):
        ua = _ua(IonQClient(api_key="key", extension=ClientExtension(user_agent_token="qiskit-ionq/1.1.0")))
        assert "qiskit-ionq/1.1.0" in ua
        assert ua.startswith("ionq-core/")

    def test_additional_user_agent_and_extension_both_present(self):
        ext = ClientExtension(user_agent_token="qiskit-ionq/1.1.0")
        ua = _ua(IonQClient(api_key="key", additional_user_agent="custom/2.0", extension=ext))
        assert "custom/2.0" in ua
        assert "qiskit-ionq/1.1.0" in ua

    def test_async_client_user_agent(self):
        client = IonQClient(api_key="key", extension=ClientExtension(user_agent_token="cirq-ionq/0.5.0"))
        assert "cirq-ionq/0.5.0" in client.get_async_httpx_client().headers["User-Agent"]


class TestDefaultHeaders:
    def test_headers_merged_into_sync_client(self):
        ext = ClientExtension(default_headers={"X-Qiskit-Version": "1.3.0", "X-Custom": "value"})
        h = IonQClient(api_key="key", extension=ext).get_httpx_client().headers
        assert h["X-Qiskit-Version"] == "1.3.0"
        assert h["X-Custom"] == "value"
        assert "Authorization" in h

    def test_headers_merged_into_async_client(self):
        ext = ClientExtension(default_headers={"X-Source": "test-sdk"})
        assert IonQClient(api_key="key", extension=ext).get_async_httpx_client().headers["X-Source"] == "test-sdk"

    def test_extension_headers_do_not_clobber_auth(self):
        ext = ClientExtension(default_headers={"X-Extra": "yes"})
        assert IonQClient(api_key="key", extension=ext).get_httpx_client().headers["Authorization"] == "apiKey key"


class TestTimeoutPrecedence:
    def test_extension_timeout_overrides_default(self):
        t = IonQClient(api_key="key", extension=ClientExtension(timeout=httpx.Timeout(120.0, connect=5.0)))
        assert t.get_httpx_client().timeout.read == 120.0
        assert t.get_httpx_client().timeout.connect == 5.0

    def test_caller_timeout_beats_extension(self):
        ext = ClientExtension(timeout=httpx.Timeout(120.0))
        t = IonQClient(api_key="key", timeout=httpx.Timeout(30.0), extension=ext)
        assert t.get_httpx_client().timeout.read == 30.0


class TestMaxRetriesPrecedence:
    def test_transport_created_with_explicit_retries(self):
        client = IonQClient(api_key="key", max_retries=3)
        assert isinstance(client.get_httpx_client()._transport, ErrorRaisingTransport)

    def test_extension_max_retries_zero_respected(self):
        client = IonQClient(api_key="key", extension=ClientExtension(max_retries=0))
        transport = client.get_httpx_client()._transport
        assert transport._transport.retry.total == 0


class TestRetryableStatusCodesOverride:
    def test_transport_created_with_custom_codes(self):
        ext = ClientExtension(retryable_status_codes=frozenset({429}))
        client = IonQClient(api_key="key", extension=ext)
        assert isinstance(client.get_httpx_client()._transport, ErrorRaisingTransport)


class TestEventHooks:
    def test_hook_protocol_satisfied_by_recording_hook(self):
        assert isinstance(RecordingHook(), EventHook)

    def test_async_hook_protocol_satisfied(self):
        assert isinstance(AsyncRecordingHook(), AsyncEventHook)

    def test_sync_hooks_wired_into_transport_chain(self):
        hook = RecordingHook()
        transport = (
            IonQClient(api_key="key", extension=ClientExtension(event_hooks=(hook,))).get_httpx_client()._transport
        )
        assert isinstance(transport, HookTransport)
        assert transport._hooks == (hook,)

    def test_async_hooks_wired_into_transport_chain(self):
        hook = AsyncRecordingHook()
        transport = (
            IonQClient(api_key="key", extension=ClientExtension(async_event_hooks=(hook,)))
            .get_async_httpx_client()
            ._transport
        )
        assert isinstance(transport, HookTransport)
        assert transport._hooks == (hook,)

    def test_no_hooks_skips_hook_transport(self):
        transport = IonQClient(api_key="key", extension=ClientExtension()).get_httpx_client()._transport
        assert isinstance(transport, ErrorRaisingTransport)


class TestHookTransportExecution:
    def test_hooks_called_in_order(self):
        hook1, hook2 = RecordingHook(), RecordingHook()
        response = httpx.Response(200)
        request = httpx.Request("GET", _BACKENDS_URL)

        result = HookTransport(FakeTransport(response), (hook1, hook2)).handle_request(request)

        assert result is response
        assert len(hook1.requests) == len(hook2.requests) == 1
        assert hook1.requests[0] is request
        assert hook1.responses[0] == (request, response)

    def test_hook_exception_is_swallowed(self):
        class BrokenHook:
            def on_request(self, request):
                raise RuntimeError("boom")

            def on_response(self, request, response):
                raise RuntimeError("boom")

            def on_error(self, request, error):
                raise RuntimeError("boom")

        response = httpx.Response(200)
        result = HookTransport(FakeTransport(response), (BrokenHook(),)).handle_request(
            httpx.Request("GET", _BACKENDS_URL)
        )
        assert result.status_code == 200


class TestOnErrorHook:
    def test_on_error_fires_on_exception(self):
        hook = RecordingHook()
        error = NotFoundError(404)
        request = httpx.Request("GET", _BACKENDS_URL)

        with pytest.raises(NotFoundError):
            HookTransport(FakeTransport(error), (hook,)).handle_request(request)

        assert len(hook.errors) == 1
        assert hook.errors[0] == (request, error)
        assert hook.responses == []

    def test_on_error_not_required(self):
        """Hooks without on_error are silently skipped."""

        class MinimalHook:
            def on_request(self, request):
                pass

            def on_response(self, request, response):
                pass

        with pytest.raises(NotFoundError):
            HookTransport(FakeTransport(NotFoundError(404)), (MinimalHook(),)).handle_request(
                httpx.Request("GET", _BACKENDS_URL)
            )

    async def test_async_on_error_fires(self):
        hook = AsyncRecordingHook()
        error = NotFoundError(404)
        request = httpx.Request("GET", _BACKENDS_URL)

        with pytest.raises(NotFoundError):
            await HookTransport(FakeTransport(error), (hook,)).handle_async_request(request)

        assert len(hook.errors) == 1
        assert hook.errors[0] == (request, error)

    async def test_async_on_error_not_required(self):
        """Async hooks without on_error are silently skipped."""

        class MinimalAsyncHook:
            async def on_request(self, request):
                pass

            async def on_response(self, request, response):
                pass

        transport = HookTransport(FakeTransport(NotFoundError(404)), (MinimalAsyncHook(),))
        with pytest.raises(NotFoundError):
            await transport.handle_async_request(httpx.Request("GET", _BACKENDS_URL))


class TestDebugHooks:
    def test_debug_propagates_hook_exception(self):
        class BrokenHook:
            def on_request(self, request):
                raise RuntimeError("hook failed")

        with pytest.raises(RuntimeError, match="hook failed"):
            HookTransport(FakeTransport(httpx.Response(200)), (BrokenHook(),), debug=True).handle_request(
                httpx.Request("GET", _BACKENDS_URL)
            )

    async def test_async_debug_propagates(self):
        class BrokenAsyncHook:
            async def on_request(self, request):
                raise RuntimeError("async hook failed")

        with pytest.raises(RuntimeError, match="async hook failed"):
            await HookTransport(
                FakeTransport(httpx.Response(200)), (BrokenAsyncHook(),), debug=True
            ).handle_async_request(httpx.Request("GET", _BACKENDS_URL))

    def test_debug_hooks_wired_from_extension(self):
        hook = RecordingHook()
        ext = ClientExtension(event_hooks=(hook,), debug_hooks=True)
        transport = IonQClient(api_key="key", extension=ext).get_httpx_client()._transport
        assert isinstance(transport, HookTransport)
        assert transport._debug is True


class TestAsyncHookExecution:
    async def test_async_hooks_called(self):
        hook = AsyncRecordingHook()
        response = httpx.Response(200)
        result = await HookTransport(FakeTransport(response), (hook,)).handle_async_request(
            httpx.Request("GET", _BACKENDS_URL)
        )
        assert result is response
        assert len(hook.requests) == len(hook.responses) == 1

    async def test_async_hook_exception_is_swallowed(self):
        class BrokenAsyncHook:
            async def on_request(self, request):
                raise RuntimeError("boom")

            async def on_response(self, request, response):
                raise RuntimeError("boom")

            async def on_error(self, request, error):
                raise RuntimeError("boom")

        response = httpx.Response(200)
        result = await HookTransport(FakeTransport(response), (BrokenAsyncHook(),)).handle_async_request(
            httpx.Request("GET", _BACKENDS_URL)
        )
        assert result.status_code == 200


class TestErrorMapper:
    def test_sync_mapper_translates_exception(self):
        class DownstreamError(Exception):
            pass

        def mapper(exc):
            if isinstance(exc, NotFoundError):
                return DownstreamError(f"translated: {exc}")
            return exc

        transport = HookTransport(FakeTransport(NotFoundError(404)), error_mapper=mapper)

        with pytest.raises(DownstreamError, match="translated"):
            transport.handle_request(httpx.Request("GET", _BACKENDS_URL))

    def test_sync_mapper_passthrough(self):
        transport = HookTransport(FakeTransport(NotFoundError(404)), error_mapper=lambda exc: exc)

        with pytest.raises(NotFoundError):
            transport.handle_request(httpx.Request("GET", _BACKENDS_URL))

    async def test_async_mapper_translates_exception(self):
        class DownstreamError(Exception):
            pass

        def mapper(exc):
            if isinstance(exc, APIError):
                return DownstreamError(f"mapped: {exc}")
            return exc

        transport = HookTransport(FakeTransport(NotFoundError(404)), error_mapper=mapper)

        with pytest.raises(DownstreamError, match="mapped"):
            await transport.handle_async_request(httpx.Request("GET", _BACKENDS_URL))

    def test_error_mapper_wired_in_transport_chain(self):
        ext = ClientExtension(error_mapper=lambda exc: exc)
        transport = IonQClient(api_key="key", extension=ext).get_httpx_client()._transport
        assert isinstance(transport, HookTransport)
        assert transport._error_mapper is not None

    def test_error_mapper_with_hooks_in_single_transport(self):
        hook = RecordingHook()
        ext = ClientExtension(event_hooks=(hook,), error_mapper=lambda exc: exc)
        transport = IonQClient(api_key="key", extension=ext).get_httpx_client()._transport
        assert isinstance(transport, HookTransport)
        assert transport._hooks == (hook,)
        assert transport._error_mapper is not None


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

        client = IonQClient(api_key="key", extension=ClientExtension(transport_wrapper=lambda t: MarkerTransport(t)))
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

        client = IonQClient(
            api_key="key", extension=ClientExtension(async_transport_wrapper=lambda t: MarkerAsyncTransport(t))
        )
        transport = client.get_async_httpx_client()._transport
        assert isinstance(transport, MarkerAsyncTransport)
        assert transport.was_wrapped is True


class TestAccessUnderlyingHttpxClient:
    def test_get_httpx_client_returns_httpx_client(self):
        assert isinstance(IonQClient(api_key="key").get_httpx_client(), httpx.Client)

    def test_get_async_httpx_client_returns_async_client(self):
        assert isinstance(IonQClient(api_key="key").get_async_httpx_client(), httpx.AsyncClient)

    def test_set_httpx_client_replaces(self):
        client = IonQClient(api_key="key")
        custom = httpx.Client(base_url="https://custom.example.com")
        client.set_httpx_client(custom)
        assert client.get_httpx_client() is custom
        custom.close()


class TestHookTransportClose:
    def test_close_delegates(self):
        HookTransport(FakeTransport(httpx.Response(200)), ()).close()

    async def test_aclose_delegates(self):
        await HookTransport(FakeTransport(httpx.Response(200)), ()).aclose()


class TestTransportChainOrder:
    def test_full_chain_sync(self):
        hook = RecordingHook()

        class OuterTransport(httpx.BaseTransport):
            def __init__(self, inner):
                self.inner = inner

            def handle_request(self, request):
                return self.inner.handle_request(request)

            def close(self):
                self.inner.close()

        ext = ClientExtension(event_hooks=(hook,), transport_wrapper=lambda t: OuterTransport(t))
        transport = IonQClient(api_key="key", extension=ext).get_httpx_client()._transport

        assert isinstance(transport, OuterTransport)
        assert isinstance(transport.inner, HookTransport)
        assert isinstance(transport.inner._transport, ErrorRaisingTransport)
