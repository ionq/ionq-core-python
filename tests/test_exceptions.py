import pytest

from ionq_core._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    raise_for_status,
)


class TestRaiseForStatus:
    @pytest.mark.parametrize("code", [200, 201, 204, 301])
    def test_success_codes_do_not_raise(self, code):
        raise_for_status(code)

    @pytest.mark.parametrize(
        ("code", "exc_cls"),
        [
            (400, BadRequestError),
            (401, AuthenticationError),
            (403, PermissionDeniedError),
            (404, NotFoundError),
            (429, RateLimitError),
            (500, ServerError),
            (502, ServerError),
            (503, ServerError),
        ],
    )
    def test_error_codes_raise_correct_type(self, code, exc_cls):
        with pytest.raises(exc_cls) as exc_info:
            raise_for_status(code)
        assert exc_info.value.status_code == code

    def test_400_preserves_body(self):
        with pytest.raises(BadRequestError) as exc_info:
            raise_for_status(400, {"message": "invalid"})
        assert exc_info.value.body == {"message": "invalid"}

    def test_429_preserves_retry_after(self):
        with pytest.raises(RateLimitError) as exc_info:
            raise_for_status(429, retry_after=30.0)
        assert exc_info.value.retry_after == 30.0

    def test_unknown_4xx_raises_api_error(self):
        with pytest.raises(APIError) as exc_info:
            raise_for_status(418)
        assert exc_info.value.status_code == 418


class TestExceptionHierarchy:
    @pytest.mark.parametrize("cls", [AuthenticationError, NotFoundError, RateLimitError, ServerError, BadRequestError])
    def test_all_inherit_from_api_error(self, cls):
        assert issubclass(cls, APIError)

    def test_api_error_has_status_code(self):
        exc = APIError(500, {"error": "oops"}, "Server error")
        assert exc.status_code == 500
        assert exc.body == {"error": "oops"}
        assert str(exc) == "Server error"

    def test_api_error_request_id(self):
        exc = APIError(500, request_id="req-123")
        assert exc.request_id == "req-123"

    def test_api_error_request_id_default_none(self):
        exc = APIError(500)
        assert exc.request_id is None

    def test_request_id_on_raise_for_status(self):
        with pytest.raises(ServerError) as exc_info:
            raise_for_status(500, request_id="req-456")
        assert exc_info.value.request_id == "req-456"

    def test_request_id_on_rate_limit(self):
        with pytest.raises(RateLimitError) as exc_info:
            raise_for_status(429, retry_after=10.0, request_id="req-789")
        assert exc_info.value.request_id == "req-789"
        assert exc_info.value.retry_after == 10.0
