import httpx
import pytest

from ionq_core._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from ionq_core._transport import (
    AsyncErrorRaisingTransport,
    ErrorRaisingTransport,
    _parse_retry_after,
    build_async_transport,
    build_retry,
    build_sync_transport,
)

_URL = "https://api.ionq.co/v0.4/backends"


class FakeTransport(httpx.BaseTransport):
    def __init__(self, responses):
        self._responses = list(responses)
        self.call_count = 0

    def handle_request(self, request):
        self.call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def close(self):
        pass


class FakeAsyncTransport(httpx.AsyncBaseTransport):
    def __init__(self, responses):
        self._responses = list(responses)
        self.call_count = 0

    async def handle_async_request(self, request):
        self.call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    async def aclose(self):
        pass


def _resp(status_code, headers=None, json_body=None):
    return httpx.Response(status_code, headers=headers or {}, json=json_body)


def _req(method="GET"):
    return httpx.Request(method, _URL)


def _sync(responses):
    fake = FakeTransport(responses)
    return ErrorRaisingTransport(fake), fake


def _async(responses):
    fake = FakeAsyncTransport(responses)
    return AsyncErrorRaisingTransport(fake), fake


class TestBuildRetry:
    def test_returns_retry_with_defaults(self):
        retry = build_retry()
        assert retry.total == 2

    def test_custom_max_retries(self):
        retry = build_retry(max_retries=5)
        assert retry.total == 5


class TestBuildTransport:
    def test_sync_transport_returns_error_raising(self):
        transport = build_sync_transport()
        assert isinstance(transport, ErrorRaisingTransport)

    def test_async_transport_returns_error_raising(self):
        transport = build_async_transport()
        assert isinstance(transport, AsyncErrorRaisingTransport)


class TestErrorRaisingTransport:
    def test_success_passes_through(self):
        transport, fake = _sync([_resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 1

    def test_401_raises_auth_error(self):
        transport, fake = _sync([_resp(401)])
        with pytest.raises(AuthenticationError):
            transport.handle_request(_req())
        assert fake.call_count == 1

    def test_404_raises_not_found(self):
        transport, fake = _sync([_resp(404)])
        with pytest.raises(NotFoundError):
            transport.handle_request(_req())
        assert fake.call_count == 1

    def test_429_raises_rate_limit(self):
        transport, _ = _sync([_resp(429)])
        with pytest.raises(RateLimitError):
            transport.handle_request(_req())

    def test_503_raises_server_error(self):
        transport, _ = _sync([_resp(503)])
        with pytest.raises(ServerError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.status_code == 503

    def test_error_body_parsed(self):
        transport, _ = _sync([_resp(400, json_body={"error": "Bad Request", "message": "Invalid input"})])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.body == {"error": "Bad Request", "message": "Invalid input"}

    def test_error_message_surfaced(self):
        transport, _ = _sync([_resp(404, json_body={"message": "Job not found"})])
        with pytest.raises(NotFoundError, match="Job not found"):
            transport.handle_request(_req())

    def test_timeout_raises_api_timeout(self):
        transport, _ = _sync([httpx.ReadTimeout("timed out")])
        with pytest.raises(APITimeoutError):
            transport.handle_request(_req())

    def test_connection_error_raises_api_connection(self):
        transport, _ = _sync([httpx.ConnectError("refused")])
        with pytest.raises(APIConnectionError):
            transport.handle_request(_req())

    def test_non_retryable_exc_includes_type_name(self):
        transport, _ = _sync([httpx.ReadError("broken pipe")])
        with pytest.raises(APIConnectionError, match="ReadError: broken pipe"):
            transport.handle_request(_req())

    def test_close_delegates(self):
        transport, _ = _sync([_resp(200)])
        transport.close()


class TestAsyncErrorRaisingTransport:
    async def test_success_passes_through(self):
        transport, fake = _async([_resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200
        assert fake.call_count == 1

    async def test_503_raises_server_error(self):
        transport, _ = _async([_resp(503)])
        with pytest.raises(ServerError):
            await transport.handle_async_request(_req())

    async def test_timeout_raises_api_timeout(self):
        transport, _ = _async([httpx.ReadTimeout("timed out")])
        with pytest.raises(APITimeoutError):
            await transport.handle_async_request(_req())

    async def test_connection_error_raises_api_connection(self):
        transport, _ = _async([httpx.ConnectError("refused")])
        with pytest.raises(APIConnectionError):
            await transport.handle_async_request(_req())

    async def test_network_error_raises_api_connection(self):
        transport, _ = _async([httpx.ReadError("broken pipe")])
        with pytest.raises(APIConnectionError, match="ReadError: broken pipe"):
            await transport.handle_async_request(_req())

    async def test_aclose_delegates(self):
        transport, _ = _async([_resp(200)])
        await transport.aclose()


class TestRequestIdOnExceptions:
    def test_request_id_from_response_header(self):
        transport, _ = _sync([_resp(404, headers={"x-request-id": "req-abc-123"})])
        with pytest.raises(NotFoundError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id == "req-abc-123"

    def test_request_id_none_when_header_missing(self):
        transport, _ = _sync([_resp(404)])
        with pytest.raises(NotFoundError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id is None

    def test_request_id_on_rate_limit(self):
        transport, _ = _sync([_resp(429, headers={"x-request-id": "req-xyz", "retry-after": "0"})])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.request_id == "req-xyz"


class TestParseRetryAfter:
    def test_numeric_returns_float(self):
        r = httpx.Response(429, headers={"retry-after": "5"})
        assert _parse_retry_after(r) == 5.0

    def test_negative_numeric_clamped_to_zero(self):
        r = httpx.Response(429, headers={"retry-after": "-10"})
        assert _parse_retry_after(r) == 0.0

    def test_missing_header_returns_none(self):
        r = httpx.Response(429)
        assert _parse_retry_after(r) is None

    def test_unparseable_returns_none(self):
        r = httpx.Response(429, headers={"retry-after": "not-a-number"})
        assert _parse_retry_after(r) is None
