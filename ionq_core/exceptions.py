# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Structured exceptions for the IonQ API client.

All exceptions inherit from `IonQError`. The hierarchy is:

```
IonQError
+-- APIConnectionError          # network / DNS failures
|   +-- APITimeoutError         # request timed out
+-- APIError                    # HTTP 4xx / 5xx responses
|   +-- BadRequestError         # 400
|   +-- AuthenticationError     # 401
|   +-- PermissionDeniedError   # 403
|   +-- NotFoundError           # 404
|   +-- RateLimitError          # 429 (includes retry_after)
|   +-- ServerError             # 5xx
```

Example:
    ```python
    from ionq_core import IonQClient, RateLimitError, AuthenticationError

    client = IonQClient()
    try:
        job = create_job.sync(client=client, body=payload)
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError as e:
        print(f"Rate limited, retry after {e.retry_after}s")
    ```
"""

__all__ = [
    "APIConnectionError",
    "APIError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "IonQError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
]


class IonQError(Exception):
    """Base exception for all IonQ errors.

    Catch this to handle any error raised by the library, including connection
    failures, API errors, polling timeouts, and job failures.
    """


class APIConnectionError(IonQError):
    """Raised when a connection to the IonQ API cannot be established.

    This covers DNS resolution failures, refused connections, and other
    network-level errors. The original ``httpx`` exception is chained
    via ``__cause__``.
    """


class APITimeoutError(APIConnectionError):
    """Raised when a request to the IonQ API times out.

    Inherits from `APIConnectionError` so that catching connection errors
    also catches timeouts.
    """


class APIError(IonQError):
    """Raised when the IonQ API returns an HTTP error response (4xx or 5xx).

    Attributes:
        status_code: The HTTP status code.
        body: The parsed response body (``dict`` if JSON, ``str`` otherwise,
            or ``None`` if the body could not be read).
        message: A human-readable error message extracted from the response,
            or a default ``"HTTP <status>"`` string.
        request_id: The ``x-request-id`` header from the response, useful for
            contacting IonQ support about a specific request.
    """

    def __init__(
        self,
        status_code: int,
        body: dict | str | None = None,
        message: str | None = None,
        *,
        request_id: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.body = body
        self.request_id = request_id
        self.message = message or f"HTTP {status_code}"
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Raised on ``401 Unauthorized``.

    Typically means the API key is missing, invalid, or revoked.
    """


class PermissionDeniedError(APIError):
    """Raised on ``403 Forbidden``.

    The API key is valid but lacks permission for the requested operation.
    """


class NotFoundError(APIError):
    """Raised on ``404 Not Found``.

    The requested resource (job, session, backend, etc.) does not exist.
    """


class BadRequestError(APIError):
    """Raised on ``400 Bad Request``.

    The request body or query parameters failed server-side validation.
    Inspect ``body`` for details.
    """


class RateLimitError(APIError):
    """Raised on ``429 Too Many Requests``.

    The client has exceeded the API rate limit. The ``retry_after`` attribute
    indicates how many seconds to wait before retrying, if the server provided
    a ``Retry-After`` header.

    Attributes:
        retry_after: Seconds to wait before retrying, or ``None`` if the
            server did not include a usable ``Retry-After`` header. The
            default transport validates the header and caps the value at
            300 seconds (non-finite values are treated as absent), so a
            hostile or buggy server cannot steer callers that sleep on this
            attribute into an unbounded wait.
    """

    def __init__(
        self,
        status_code: int = 429,
        body: dict | str | None = None,
        message: str | None = None,
        retry_after: float | None = None,
        *,
        request_id: str | None = None,
    ) -> None:
        super().__init__(status_code, body, message, request_id=request_id)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised on ``5xx`` server errors.

    These are typically transient and are automatically retried by the default
    transport (see `IonQClient`).
    """


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
    *,
    request_id: str | None = None,
) -> None:
    """Raise an appropriate `APIError` subclass for an HTTP error status.

    Does nothing for status codes below 400. For 4xx codes, raises the
    specific subclass (e.g. `AuthenticationError` for 401). For 5xx codes
    or unrecognized 4xx codes, raises `ServerError` or `APIError` respectively.

    Args:
        status_code: The HTTP status code.
        body: The parsed response body.
        retry_after: Value from the ``Retry-After`` header, if present.
        message: A human-readable error message.
        request_id: The ``x-request-id`` response header.

    Raises:
        BadRequestError: On 400.
        AuthenticationError: On 401.
        PermissionDeniedError: On 403.
        NotFoundError: On 404.
        RateLimitError: On 429.
        ServerError: On 5xx.
        APIError: On other 4xx codes.
    """
    if status_code < 400:
        return
    exc_cls = _STATUS_TO_EXCEPTION.get(status_code, ServerError if status_code >= 500 else APIError)
    if exc_cls is RateLimitError:
        raise RateLimitError(status_code, body, message, retry_after, request_id=request_id)
    raise exc_cls(status_code, body, message, request_id=request_id)
