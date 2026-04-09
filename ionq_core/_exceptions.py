"""Structured exceptions for the IonQ API client."""


class IonQError(Exception):
    """Base exception for all IonQ API errors."""


class APIConnectionError(IonQError):
    """Raised when a connection to the IonQ API cannot be established."""


class APITimeoutError(APIConnectionError):
    """Raised when a request to the IonQ API times out."""


class APIError(IonQError):
    """Raised when the IonQ API returns an error response.

    Attributes:
        status_code: HTTP status code.
        body: Parsed response body, if available.
        message: Human-readable error message.
    """

    def __init__(self, status_code: int, body: dict | str | None = None, message: str | None = None) -> None:
        self.status_code = status_code
        self.body = body
        self.message = message or f"HTTP {status_code}"
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Raised on 401 Unauthorized."""


class PermissionDeniedError(APIError):
    """Raised on 403 Forbidden."""


class NotFoundError(APIError):
    """Raised on 404 Not Found."""


class BadRequestError(APIError):
    """Raised on 400 Bad Request."""


class RateLimitError(APIError):
    """Raised on 429 Too Many Requests.

    Attributes:
        retry_after: Seconds to wait before retrying, from Retry-After header.
    """

    retry_after: float | None = None


class ServerError(APIError):
    """Raised on 500, 502, or 503."""


_STATUS_TO_EXCEPTION: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    429: RateLimitError,
}


def raise_for_status(
    status_code: int,
    body: dict | str | None = None,
    retry_after: float | None = None,
    message: str | None = None,
) -> None:
    """Raise the appropriate exception for an error status code."""
    if status_code < 400:
        return

    exc_cls = _STATUS_TO_EXCEPTION.get(status_code)
    if exc_cls is None:
        exc_cls = ServerError if status_code >= 500 else APIError

    exc = exc_cls(status_code, body, message)
    if isinstance(exc, RateLimitError):
        exc.retry_after = retry_after
    raise exc
