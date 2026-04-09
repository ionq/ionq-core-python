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
    def test_200_does_not_raise(self):
        raise_for_status(200)

    def test_201_does_not_raise(self):
        raise_for_status(201)

    def test_400_raises_bad_request(self):
        with pytest.raises(BadRequestError) as exc_info:
            raise_for_status(400, {"message": "invalid"})
        assert exc_info.value.status_code == 400
        assert exc_info.value.body == {"message": "invalid"}

    def test_401_raises_authentication_error(self):
        with pytest.raises(AuthenticationError):
            raise_for_status(401)

    def test_403_raises_permission_denied(self):
        with pytest.raises(PermissionDeniedError):
            raise_for_status(403)

    def test_404_raises_not_found(self):
        with pytest.raises(NotFoundError):
            raise_for_status(404)

    def test_429_raises_rate_limit(self):
        with pytest.raises(RateLimitError) as exc_info:
            raise_for_status(429, retry_after=30.0)
        assert exc_info.value.retry_after == 30.0

    def test_500_raises_server_error(self):
        with pytest.raises(ServerError):
            raise_for_status(500)

    def test_502_raises_server_error(self):
        with pytest.raises(ServerError):
            raise_for_status(502)

    def test_503_raises_server_error(self):
        with pytest.raises(ServerError):
            raise_for_status(503)

    def test_418_raises_api_error(self):
        with pytest.raises(APIError) as exc_info:
            raise_for_status(418)
        assert exc_info.value.status_code == 418


class TestExceptionHierarchy:
    def test_all_inherit_from_api_error(self):
        for exc_cls in (AuthenticationError, NotFoundError, RateLimitError, ServerError, BadRequestError):
            assert issubclass(exc_cls, APIError)

    def test_api_error_has_status_code(self):
        exc = APIError(500, {"error": "oops"}, "Server error")
        assert exc.status_code == 500
        assert exc.body == {"error": "oops"}
        assert str(exc) == "Server error"
