import httpx
import pytest

from ionq_core._transport import ErrorRaisingTransport, build_transport
from ionq_core.exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from tests.conftest import BASE_URL

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


class TestBuildTransport:
    def test_returns_error_raising(self):
        assert isinstance(build_transport(), ErrorRaisingTransport)

    def test_retries_post_requests(self):
        transport = build_transport()
        retry = transport._transport.retry
        assert "POST" in retry.allowed_methods


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
