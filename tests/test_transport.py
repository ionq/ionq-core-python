import ssl

import httpx
import pytest

from ionq_core._transport import (
    MAX_ERROR_BODY_BYTES,
    MAX_RETRY_AFTER,
    ErrorRaisingTransport,
    build_transport,
)
from ionq_core.exceptions import (
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from tests.conftest import BASE_URL, FakeTransport

_URL = f"{BASE_URL}/backends"


def _resp(status_code, headers=None, json_body=None):
    return httpx.Response(status_code, headers=headers or {}, json=json_body)


def _req(method="GET"):
    return httpx.Request(method, _URL)


def _wrap(responses):
    fake = FakeTransport(*responses)
    return ErrorRaisingTransport(fake), fake


class TestBuildTransport:
    def test_does_not_retry_post_requests(self):
        # POSTs are billable and the API has no idempotency keys, so retrying an ambiguous 5xx could duplicate work.
        transport = build_transport()
        retry = transport._transport.retry
        assert "POST" not in retry.allowed_methods
        assert "GET" in retry.allowed_methods

    def test_sync_and_async_share_retry_config(self):
        transport = build_transport(max_retries=5)
        assert transport._transport.retry.total == 5
        assert transport._async_transport.retry.total == 5


class TestBuildTransportTls:
    @staticmethod
    def _ssl_contexts(transport):
        sync_ctx = transport._transport._sync_transport._pool._ssl_context
        async_ctx = transport._async_transport._async_transport._pool._ssl_context
        return sync_ctx, async_ctx

    def test_default_verifies_certificates(self):
        sync_ctx, async_ctx = self._ssl_contexts(build_transport())
        assert sync_ctx is async_ctx  # built once, shared by both transports
        assert sync_ctx.verify_mode == ssl.CERT_REQUIRED

    def test_verify_false_disables_verification(self):
        for ctx in self._ssl_contexts(build_transport(verify=False)):
            assert ctx.verify_mode == ssl.CERT_NONE

    def test_custom_ssl_context_used_verbatim(self):
        pinned = ssl.create_default_context()
        for ctx in self._ssl_contexts(build_transport(verify=pinned)):
            assert ctx is pinned


class TestErrorRaisingTransportSync:
    def test_success_passes_through(self):
        transport, fake = _wrap([_resp(200)])
        assert transport.handle_request(_req()).status_code == 200
        assert fake.call_count == 1

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

    @pytest.mark.parametrize("key", ["message", "error"])
    def test_error_message_surfaced(self, key):
        transport, _ = _wrap([_resp(404, json_body={key: "Job not found"})])
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

    @pytest.mark.parametrize(
        ("header", "expected"),
        [
            ("9000000000", MAX_RETRY_AFTER),  # large finite values are capped
            (str(MAX_RETRY_AFTER + 1), MAX_RETRY_AFTER),
            ("-3", 0.0),  # negative values are floored
            ("inf", None),
            ("1e309", None),  # overflows float() to +inf
            ("nan", None),
        ],
    )
    def test_retry_after_bounded(self, header, expected):
        # Callers sleep on retry_after, so a forged header must never cause an unbounded or non-finite wait (CWE-1284).
        transport, _ = _wrap([_resp(429, headers={"retry-after": header})])
        with pytest.raises(RateLimitError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.retry_after == expected


class _CountingStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    """Large streamed body that counts the chunks consumed."""

    def __init__(self, chunk_size=16384, chunks=1000):
        self.chunk = b"x" * chunk_size
        self.chunks = chunks
        self.consumed = 0

    def __iter__(self):
        for _ in range(self.chunks):
            self.consumed += 1
            yield self.chunk

    async def __aiter__(self):
        for chunk in self:
            yield chunk


class TestErrorBodyCap:
    """Error bodies are server-controlled; only a bounded prefix may be read (CWE-409)."""

    # chunks needed to reach the cap, +1 for iteration slack
    _MAX_CHUNKS = MAX_ERROR_BODY_BYTES // 16384 + 1

    def test_sync_read_stops_at_cap(self):
        stream = _CountingStream()
        transport, _ = _wrap([httpx.Response(400, stream=stream)])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert stream.consumed <= self._MAX_CHUNKS
        assert len(exc_info.value.body) <= 500

    async def test_async_read_stops_at_cap(self):
        stream = _CountingStream()
        transport, _ = _wrap([httpx.Response(400, stream=stream)])
        with pytest.raises(BadRequestError) as exc_info:
            await transport.handle_async_request(_req())
        assert stream.consumed <= self._MAX_CHUNKS
        assert len(exc_info.value.body) <= 500

    def test_plain_text_body_truncated_to_500(self):
        transport, _ = _wrap([httpx.Response(400, content=b"e" * 600)])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert exc_info.value.body == "e" * 500

    def test_json_body_exceeding_cap_degrades_to_text(self):
        # Truncation invalidates the JSON, so the capped prefix is surfaced as text.
        big = b'{"message": "' + b"a" * (MAX_ERROR_BODY_BYTES + 1000) + b'"}'
        transport, _ = _wrap([httpx.Response(400, content=big)])
        with pytest.raises(BadRequestError) as exc_info:
            transport.handle_request(_req())
        assert isinstance(exc_info.value.body, str)
        assert len(exc_info.value.body) <= 500
