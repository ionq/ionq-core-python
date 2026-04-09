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


class FakeTransport(httpx.BaseTransport):
    """Transport that returns a sequence of responses/exceptions."""

    def __init__(self, responses):
        self._responses = list(responses)
        self._call_count = 0

    def handle_request(self, request):
        self._call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def close(self):
        pass


def _response(status_code, headers=None, json_body=None):
    return httpx.Response(status_code, headers=dict(headers or {}), json=json_body)


def _request():
    return httpx.Request("GET", "https://api.ionq.co/v0.4/backends")


class TestRetryTransport:
    def _make_transport(self, responses, max_retries=2):
        fake = FakeTransport(responses)
        return RetryTransport(fake, max_retries=max_retries), fake

    def test_success_no_retry(self):
        transport, fake = self._make_transport([_response(200)])
        resp = transport.handle_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 1

    def test_retries_on_503_then_succeeds(self):
        transport, fake = self._make_transport([_response(503), _response(200)])
        resp = transport.handle_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 2

    def test_retries_on_429_then_succeeds(self):
        transport, fake = self._make_transport([
            _response(429, headers={"retry-after": "0"}),
            _response(200),
        ])
        resp = transport.handle_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 2

    def test_retries_exhausted_raises_server_error(self):
        transport, fake = self._make_transport(
            [_response(503), _response(503), _response(503)],
            max_retries=2,
        )
        with pytest.raises(ServerError) as exc_info:
            transport.handle_request(_request())
        assert exc_info.value.status_code == 503
        assert fake._call_count == 3

    def test_retries_exhausted_rate_limit(self):
        transport, fake = self._make_transport(
            [_response(429), _response(429), _response(429)],
            max_retries=2,
        )
        with pytest.raises(RateLimitError):
            transport.handle_request(_request())
        assert fake._call_count == 3

    def test_connection_error_retried(self):
        transport, fake = self._make_transport([httpx.ConnectError("refused"), _response(200)])
        resp = transport.handle_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 2

    def test_timeout_error_retried(self):
        transport, fake = self._make_transport([httpx.ReadTimeout("timed out"), _response(200)])
        resp = transport.handle_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 2

    def test_timeout_exhausted_raises(self):
        transport, _ = self._make_transport(
            [httpx.ReadTimeout("timed out")] * 3,
            max_retries=2,
        )
        with pytest.raises(APITimeoutError):
            transport.handle_request(_request())

    def test_connection_exhausted_raises(self):
        transport, _ = self._make_transport(
            [httpx.ConnectError("refused")] * 3,
            max_retries=2,
        )
        with pytest.raises(APIConnectionError):
            transport.handle_request(_request())

    def test_401_not_retried(self):
        transport, fake = self._make_transport([_response(401)])
        with pytest.raises(AuthenticationError):
            transport.handle_request(_request())
        assert fake._call_count == 1

    def test_404_not_retried(self):
        transport, fake = self._make_transport([_response(404)])
        with pytest.raises(NotFoundError):
            transport.handle_request(_request())
        assert fake._call_count == 1

    def test_max_retries_zero(self):
        transport, fake = self._make_transport([_response(503)], max_retries=0)
        with pytest.raises(ServerError):
            transport.handle_request(_request())
        assert fake._call_count == 1

    def test_error_body_parsed(self):
        transport, _ = self._make_transport([
            _response(400, json_body={"error": "Bad Request", "message": "Invalid input"}),
        ])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_request())
        assert exc_info.value.body == {"error": "Bad Request", "message": "Invalid input"}

    def test_error_message_surfaced(self):
        transport, _ = self._make_transport([
            _response(404, json_body={"message": "Job not found"}),
        ])
        with pytest.raises(NotFoundError, match="Job not found"):
            transport.handle_request(_request())

    def test_retry_after_header_respected(self, monkeypatch):
        sleeps = []
        monkeypatch.setattr("ionq_core._transport.time.sleep", sleeps.append)
        transport, _ = self._make_transport([
            _response(429, headers={"retry-after": "10"}),
            _response(200),
        ])
        transport.handle_request(_request())
        assert sleeps[0] >= 10.0


class FakeAsyncTransport(httpx.AsyncBaseTransport):
    def __init__(self, responses):
        self._responses = list(responses)
        self._call_count = 0

    async def handle_async_request(self, request):
        self._call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    async def aclose(self):
        pass


class TestAsyncRetryTransport:
    def _make_transport(self, responses, max_retries=2):
        fake = FakeAsyncTransport(responses)
        return AsyncRetryTransport(fake, max_retries=max_retries), fake

    async def test_success_no_retry(self):
        transport, fake = self._make_transport([_response(200)])
        resp = await transport.handle_async_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 1

    async def test_retries_on_503_then_succeeds(self):
        transport, fake = self._make_transport([_response(503), _response(200)])
        resp = await transport.handle_async_request(_request())
        assert resp.status_code == 200
        assert fake._call_count == 2

    async def test_retries_exhausted_raises(self):
        transport, fake = self._make_transport(
            [_response(503), _response(503), _response(503)],
            max_retries=2,
        )
        with pytest.raises(ServerError):
            await transport.handle_async_request(_request())
        assert fake._call_count == 3

    async def test_timeout_retried(self):
        transport, fake = self._make_transport([httpx.ReadTimeout("timed out"), _response(200)])
        resp = await transport.handle_async_request(_request())
        assert resp.status_code == 200
