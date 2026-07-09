import ssl

import httpx
import pytest
from httpx_retries import Retry, RetryTransport

from ionq_core._transport import (
    PRE_SEND_EXCEPTIONS,
    RETRYABLE_STATUS_CODES,
    DualTransport,
    ErrorRaisingTransport,
    NonIdempotentRetry,
    _retry_stack,
    build_transport,
)
from ionq_core.exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from tests.conftest import BASE_URL, socket_transports

_URL = f"{BASE_URL}/backends"


class FakeTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    def __init__(self, responses):
        self._responses = list(responses)
        self.call_count = 0

    def _next(self):
        self.call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def handle_request(self, request):
        return self._next()

    async def handle_async_request(self, request):
        return self._next()


def _resp(status_code, headers=None, json_body=None):
    return httpx.Response(status_code, headers=headers or {}, json=json_body)


def _req(method="GET"):
    return httpx.Request(method, _URL)


def _wrap(responses):
    fake = FakeTransport(responses)
    return ErrorRaisingTransport(fake), fake


def _stack(responses, max_retries=2):
    fake = FakeTransport(responses)
    return _retry_stack(fake, max_retries, RETRYABLE_STATUS_CODES), fake


@pytest.fixture
def no_retry_sleep(monkeypatch):
    async def _asleep(self, response):
        return None

    monkeypatch.setattr(Retry, "sleep", lambda self, response: None)
    monkeypatch.setattr(Retry, "asleep", _asleep)


class TestBuildTransport:
    def test_returns_error_raising(self):
        assert isinstance(build_transport(), ErrorRaisingTransport)

    def test_post_policy_is_pre_send_only(self):
        outer = build_transport()._transport
        assert isinstance(outer, RetryTransport)
        assert isinstance(outer.retry, NonIdempotentRetry)
        assert outer.retry.allowed_methods == frozenset({"POST"})
        assert not outer.retry.is_retryable_status_code(503)
        assert outer.retry.retryable_exceptions == PRE_SEND_EXCEPTIONS

    def test_idempotent_policy_excludes_post(self):
        inner = build_transport()._transport._sync_transport
        assert isinstance(inner, RetryTransport)
        assert "POST" not in inner.retry.allowed_methods
        assert inner.retry.status_forcelist == RETRYABLE_STATUS_CODES
        assert inner.retry.is_retryable_status_code(503)

    def test_verify_context_reaches_socket_transports(self):
        ctx = ssl.create_default_context()
        sync_t, async_t = socket_transports(build_transport(verify=ctx))
        assert sync_t._pool._ssl_context is ctx
        assert async_t._pool._ssl_context is ctx

    def test_verify_default_enforces_verification(self):
        sync_t, async_t = socket_transports(build_transport())
        assert sync_t._pool._ssl_context.verify_mode == ssl.CERT_REQUIRED
        assert async_t._pool._ssl_context.verify_mode == ssl.CERT_REQUIRED

    def test_close_full_stack(self):
        build_transport().close()

    async def test_aclose_full_stack(self):
        await build_transport().aclose()


@pytest.mark.usefixtures("no_retry_sleep")
class TestRetryPolicySync:
    def test_post_not_resent_after_retryable_status(self):
        stack, fake = _stack([_resp(503), _resp(200)])
        assert stack.handle_request(_req("POST")).status_code == 503
        assert fake.call_count == 1

    def test_post_not_resent_after_429(self):
        stack, fake = _stack([_resp(429, headers={"retry-after": "0"}), _resp(200)])
        assert stack.handle_request(_req("POST")).status_code == 429
        assert fake.call_count == 1

    def test_get_retried_on_retryable_status(self):
        stack, fake = _stack([_resp(503), _resp(200)])
        assert stack.handle_request(_req("GET")).status_code == 200
        assert fake.call_count == 2

    def test_get_retried_on_read_timeout(self):
        stack, fake = _stack([httpx.ReadTimeout("timed out"), _resp(200)])
        assert stack.handle_request(_req("GET")).status_code == 200
        assert fake.call_count == 2

    def test_get_returns_last_response_when_exhausted(self):
        stack, fake = _stack([_resp(503), _resp(503), _resp(503)])
        assert stack.handle_request(_req("GET")).status_code == 503
        assert fake.call_count == 3

    @pytest.mark.parametrize(
        "exc",
        [httpx.ConnectError("refused"), httpx.ConnectTimeout("connect"), httpx.PoolTimeout("pool")],
        ids=["connect-error", "connect-timeout", "pool-timeout"],
    )
    def test_post_retried_on_pre_send_failure(self, exc):
        stack, fake = _stack([exc, _resp(200)])
        assert stack.handle_request(_req("POST")).status_code == 200
        assert fake.call_count == 2

    def test_post_not_retried_on_read_timeout(self):
        stack, fake = _stack([httpx.ReadTimeout("timed out"), _resp(200)])
        with pytest.raises(httpx.ReadTimeout):
            stack.handle_request(_req("POST"))
        assert fake.call_count == 1

    def test_post_not_retried_on_remote_protocol_error(self):
        stack, fake = _stack([httpx.RemoteProtocolError("server disconnected"), _resp(200)])
        with pytest.raises(httpx.RemoteProtocolError):
            stack.handle_request(_req("POST"))
        assert fake.call_count == 1

    def test_post_zero_retries(self):
        stack, fake = _stack([httpx.ConnectError("refused")], max_retries=0)
        with pytest.raises(httpx.ConnectError):
            stack.handle_request(_req("POST"))
        assert fake.call_count == 1


@pytest.mark.usefixtures("no_retry_sleep")
class TestRetryPolicyAsync:
    async def test_post_not_resent_after_retryable_status(self):
        stack, fake = _stack([_resp(503), _resp(200)])
        assert (await stack.handle_async_request(_req("POST"))).status_code == 503
        assert fake.call_count == 1

    async def test_post_retried_on_connect_error(self):
        stack, fake = _stack([httpx.ConnectError("refused"), _resp(200)])
        assert (await stack.handle_async_request(_req("POST"))).status_code == 200
        assert fake.call_count == 2

    async def test_get_retried_on_retryable_status(self):
        stack, fake = _stack([_resp(503), _resp(200)])
        assert (await stack.handle_async_request(_req("GET"))).status_code == 200
        assert fake.call_count == 2


class TestDualTransport:
    def test_sync_requests_use_sync_transport(self):
        dual = DualTransport(FakeTransport([_resp(200)]), FakeTransport([_resp(201)]))
        assert dual.handle_request(_req()).status_code == 200
        dual.close()

    async def test_async_requests_use_async_transport(self):
        dual = DualTransport(FakeTransport([_resp(200)]), FakeTransport([_resp(201)]))
        assert (await dual.handle_async_request(_req())).status_code == 201
        await dual.aclose()


class TestErrorRaisingTransportSync:
    def test_success_passes_through(self):
        transport, fake = _wrap([_resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 1

    def test_401_raises_auth_error(self):
        transport, _ = _wrap([_resp(401)])
        with pytest.raises(AuthenticationError):
            transport.handle_request(_req())

    def test_404_raises_not_found(self):
        transport, _ = _wrap([_resp(404)])
        with pytest.raises(NotFoundError):
            transport.handle_request(_req())

    def test_429_raises_rate_limit(self):
        transport, _ = _wrap([_resp(429)])
        with pytest.raises(RateLimitError):
            transport.handle_request(_req())

    def test_503_raises_server_error(self):
        transport, _ = _wrap([_resp(503)])
        with pytest.raises(ServerError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.status_code == 503

    def test_error_body_parsed(self):
        transport, _ = _wrap([_resp(400, json_body={"error": "Bad Request", "message": "Invalid input"})])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.body == {"error": "Bad Request", "message": "Invalid input"}

    def test_error_message_surfaced(self):
        transport, _ = _wrap([_resp(404, json_body={"message": "Job not found"})])
        with pytest.raises(NotFoundError, match="Job not found"):
            transport.handle_request(_req())

    def test_timeout_raises_api_timeout(self):
        transport, _ = _wrap([httpx.ReadTimeout("timed out")])
        with pytest.raises(APITimeoutError):
            transport.handle_request(_req())

    def test_connection_error_raises_api_connection(self):
        transport, _ = _wrap([httpx.ConnectError("refused")])
        with pytest.raises(APIConnectionError):
            transport.handle_request(_req())

    def test_exc_type_name_in_message(self):
        transport, _ = _wrap([httpx.ReadError("broken pipe")])
        with pytest.raises(APIConnectionError, match="ReadError: broken pipe"):
            transport.handle_request(_req())

    def test_close_delegates(self):
        transport, _ = _wrap([_resp(200)])
        transport.close()


class TestErrorRaisingTransportAsync:
    async def test_success_passes_through(self):
        transport, fake = _wrap([_resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200
        assert fake.call_count == 1

    async def test_503_raises_server_error(self):
        transport, _ = _wrap([_resp(503)])
        with pytest.raises(ServerError):
            await transport.handle_async_request(_req())

    async def test_timeout_raises_api_timeout(self):
        transport, _ = _wrap([httpx.ReadTimeout("timed out")])
        with pytest.raises(APITimeoutError):
            await transport.handle_async_request(_req())

    async def test_connection_error_raises_api_connection(self):
        transport, _ = _wrap([httpx.ConnectError("refused")])
        with pytest.raises(APIConnectionError):
            await transport.handle_async_request(_req())

    async def test_exc_type_name_in_message(self):
        transport, _ = _wrap([httpx.ReadError("broken pipe")])
        with pytest.raises(APIConnectionError, match="ReadError: broken pipe"):
            await transport.handle_async_request(_req())

    async def test_aclose_delegates(self):
        transport, _ = _wrap([_resp(200)])
        await transport.aclose()


class TestRequestId:
    def test_from_response_header(self):
        transport, _ = _wrap([_resp(404, headers={"x-request-id": "req-abc-123"})])
        with pytest.raises(NotFoundError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id == "req-abc-123"

    def test_none_when_header_missing(self):
        transport, _ = _wrap([_resp(404)])
        with pytest.raises(NotFoundError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id is None

    def test_on_rate_limit(self):
        transport, _ = _wrap([_resp(429, headers={"x-request-id": "req-xyz", "retry-after": "0"})])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id == "req-xyz"


class TestRetryAfterParsing:
    def test_numeric_retry_after_on_rate_limit(self):
        transport, _ = _wrap([_resp(429, headers={"retry-after": "5"})])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.retry_after == 5.0

    def test_missing_retry_after(self):
        transport, _ = _wrap([_resp(429)])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.retry_after is None

    def test_unparseable_retry_after(self):
        transport, _ = _wrap([_resp(429, headers={"retry-after": "not-a-number"})])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.retry_after is None
