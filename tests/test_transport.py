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
from ionq_core._transport import AsyncRetryTransport, RetryTransport

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


def _sync(responses, max_retries=2):
    fake = FakeTransport(responses)
    return RetryTransport(fake, max_retries=max_retries), fake


def _async(responses, max_retries=2):
    fake = FakeAsyncTransport(responses)
    return AsyncRetryTransport(fake, max_retries=max_retries), fake


class TestRetryTransport:
    def test_success_no_retry(self):
        transport, fake = _sync([_resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 1

    def test_retries_on_503_then_succeeds(self):
        transport, fake = _sync([_resp(503), _resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 2

    def test_retries_on_429_then_succeeds(self):
        transport, fake = _sync([_resp(429, headers={"retry-after": "0"}), _resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 2

    def test_retries_exhausted_raises_server_error(self):
        transport, fake = _sync([_resp(503)] * 3, max_retries=2)
        with pytest.raises(ServerError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.status_code == 503
        assert fake.call_count == 3

    def test_retries_exhausted_rate_limit(self):
        transport, fake = _sync([_resp(429)] * 3, max_retries=2)
        with pytest.raises(RateLimitError):
            transport.handle_request(_req())
        assert fake.call_count == 3

    def test_connection_error_retried(self):
        transport, fake = _sync([httpx.ConnectError("refused"), _resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 2

    def test_timeout_error_retried(self):
        transport, fake = _sync([httpx.ReadTimeout("timed out"), _resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 2

    def test_timeout_exhausted_raises(self):
        transport, _ = _sync([httpx.ReadTimeout("timed out")] * 3, max_retries=2)
        with pytest.raises(APITimeoutError):
            transport.handle_request(_req())

    def test_connection_exhausted_raises(self):
        transport, _ = _sync([httpx.ConnectError("refused")] * 3, max_retries=2)
        with pytest.raises(APIConnectionError):
            transport.handle_request(_req())

    def test_401_not_retried(self):
        transport, fake = _sync([_resp(401)])
        with pytest.raises(AuthenticationError):
            transport.handle_request(_req())
        assert fake.call_count == 1

    def test_404_not_retried(self):
        transport, fake = _sync([_resp(404)])
        with pytest.raises(NotFoundError):
            transport.handle_request(_req())
        assert fake.call_count == 1

    def test_max_retries_zero(self):
        transport, fake = _sync([_resp(503)], max_retries=0)
        with pytest.raises(ServerError):
            transport.handle_request(_req())
        assert fake.call_count == 1

    def test_error_body_parsed(self):
        transport, _ = _sync([_resp(400, json_body={"error": "Bad Request", "message": "Invalid input"})])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.body == {"error": "Bad Request", "message": "Invalid input"}

    def test_error_message_surfaced(self):
        transport, _ = _sync([_resp(404, json_body={"message": "Job not found"})])
        with pytest.raises(NotFoundError, match="Job not found"):
            transport.handle_request(_req())

    def test_retry_after_header_respected(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr("ionq_core._transport.time.sleep", sleeps.append)
        transport, _ = _sync([_resp(429, headers={"retry-after": "10"}), _resp(200)])
        transport.handle_request(_req())
        assert sleeps[0] >= 10.0


class TestAsyncRetryTransport:
    async def test_success_no_retry(self):
        transport, fake = _async([_resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200
        assert fake.call_count == 1

    async def test_retries_on_503_then_succeeds(self):
        transport, fake = _async([_resp(503), _resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200
        assert fake.call_count == 2

    async def test_retries_exhausted_raises(self):
        transport, fake = _async([_resp(503)] * 3, max_retries=2)
        with pytest.raises(ServerError):
            await transport.handle_async_request(_req())
        assert fake.call_count == 3

    async def test_timeout_retried(self):
        transport, _ = _async([httpx.ReadTimeout("timed out"), _resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200


class TestRetryAfterDateHeader:
    def test_retry_after_http_date(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr("ionq_core._transport.time.sleep", sleeps.append)
        monkeypatch.setattr("ionq_core._transport.time.time", lambda: 1000.0)
        monkeypatch.setattr("ionq_core._transport.calendar.timegm", lambda _: 1005.0)
        transport, _ = _sync(
            [_resp(429, headers={"retry-after": "Mon, 01 Jan 2030 00:00:00 GMT"}), _resp(200)]
        )
        transport.handle_request(_req())
        assert sleeps[0] >= 5.0

    def test_retry_after_unparseable_ignored(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr("ionq_core._transport.time.sleep", sleeps.append)
        transport, _ = _sync([_resp(429, headers={"retry-after": "not-a-date-or-number"}), _resp(200)])
        transport.handle_request(_req())
        assert len(sleeps) == 1


class TestRaiseExhaustedEdgeCases:
    def test_no_response_no_exception(self):
        from ionq_core._transport import _raise_exhausted

        with pytest.raises(APIConnectionError, match="no response"):
            _raise_exhausted(None, None)


class TestRetryableExcEdgeCases:
    def test_post_timeout_not_retried(self):
        transport, fake = _sync([httpx.ReadTimeout("timed out")])
        with pytest.raises(APIConnectionError):
            transport.handle_request(_req("POST"))
        assert fake.call_count == 1


class TestAsyncRetryTransportEdgeCases:
    async def test_connection_error_retried(self):
        transport, fake = _async([httpx.ConnectError("refused"), _resp(200)])
        assert (await transport.handle_async_request(_req())).status_code == 200
        assert fake.call_count == 2

    async def test_non_retryable_exc_raises(self):
        transport, _ = _async([RuntimeError("unexpected")])
        with pytest.raises(APIConnectionError):
            await transport.handle_async_request(_req())

    async def test_aclose_delegates(self):
        transport, _ = _async([_resp(200)])
        await transport.aclose()


class TestIdempotencyAwareRetry:
    def test_post_503_not_retried(self):
        transport, fake = _sync([_resp(503)])
        with pytest.raises(ServerError):
            transport.handle_request(_req("POST"))
        assert fake.call_count == 1

    def test_post_429_retried(self):
        transport, fake = _sync([_resp(429), _resp(200)])
        assert transport.handle_request(_req("POST")).status_code == 200
        assert fake.call_count == 2

    def test_get_503_retried(self):
        transport, fake = _sync([_resp(503), _resp(200)])
        assert transport.handle_request(_req("GET")).status_code == 200
        assert fake.call_count == 2

    def test_put_503_retried(self):
        transport, fake = _sync([_resp(503), _resp(200)])
        assert transport.handle_request(_req("PUT")).status_code == 200
        assert fake.call_count == 2

    def test_delete_503_retried(self):
        transport, fake = _sync([_resp(503), _resp(200)])
        assert transport.handle_request(_req("DELETE")).status_code == 200
        assert fake.call_count == 2

    def test_post_connect_error_retried(self):
        transport, fake = _sync([httpx.ConnectError("refused"), _resp(200)])
        assert transport.handle_request(_req("POST")).status_code == 200
        assert fake.call_count == 2

    def test_post_read_error_not_retried(self):
        transport, fake = _sync([httpx.ReadError("broken pipe")])
        with pytest.raises(APIConnectionError):
            transport.handle_request(_req("POST"))
        assert fake.call_count == 1
