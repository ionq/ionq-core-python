# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Structured exceptions for the IonQ API client.

All exceptions inherit from `IonQError`:

```
IonQError
+-- APIConnectionError          # network / DNS failures
|   +-- APITimeoutError         # request timed out
+-- APIError                    # HTTP 4xx / 5xx responses (carries retry_after)
|   +-- BadRequestError         # 400
|   +-- AuthenticationError     # 401
|   +-- PermissionDeniedError   # 403
|   +-- NotFoundError           # 404
|   +-- RateLimitError          # 429
|   +-- ServerError             # 5xx
+-- JobTimeoutError             # polling deadline exceeded (ionq_core.polling)
+-- JobFailedError              # polled job ended in failure (ionq_core.polling)
```

Example:
    ```python
    from ionq_core import IonQClient, RateLimitError, AuthenticationError
    from ionq_core.api.default import create_job

    client = IonQClient()
    try:
        job = create_job.sync(client=client, body=...)
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

    The only error outside this tree is ``errors.UnexpectedStatus``, raised for
    undocumented status codes when ``raise_on_unexpected_status`` is set.
    """


class APIConnectionError(IonQError):
    """Raised when a connection to the IonQ API cannot be established.

    Covers DNS failures, refused connections, and other network-level errors.
    The original ``httpx`` exception is chained via ``__cause__``.
    """


class APITimeoutError(APIConnectionError):
    """Raised when a request to the IonQ API times out.

    Also caught by ``except APIConnectionError``.
    """


class APIError(IonQError):
    """Raised when the IonQ API returns an HTTP error response (4xx or 5xx).

    Attributes:
        status_code: The HTTP status code.
        body: Parsed response body (``dict`` if JSON, ``str`` otherwise,
            ``None`` if it could not be read).
        message: Error message from the response, or ``"HTTP <status>"``.
        retry_after: Seconds to wait before retrying, from the ``Retry-After``
            header, or ``None`` if the server sent no usable one.
        request_id: The ``x-request-id`` response header; quote it when
            contacting IonQ support.
    """

    def __init__(
        self,
        status_code: int,
        body: dict | str | None = None,
        message: str | None = None,
        retry_after: float | None = None,
        *,
        request_id: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.body = body
        self.retry_after = retry_after
        self.request_id = request_id
        self.message = message or f"HTTP {status_code}"
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Raised on ``401 Unauthorized``: the API key is missing, invalid, or revoked."""


class PermissionDeniedError(APIError):
    """Raised on ``403 Forbidden``: the API key is valid but lacks permission for the operation."""


class NotFoundError(APIError):
    """Raised on ``404 Not Found``: the job, session, backend, etc. does not exist."""


class BadRequestError(APIError):
    """Raised on ``400 Bad Request``: the body or query params failed server-side validation.

    Inspect ``body`` for details.
    """


class RateLimitError(APIError):
    """Raised on ``429 Too Many Requests``.

    Attributes:
        retry_after: Seconds to wait before retrying, or ``None`` if the server
            sent no usable ``Retry-After`` header. The default transport caps
            it at 300 seconds (non-finite values count as absent), so a hostile
            or buggy server cannot push callers that sleep on it into an
            unbounded wait.
    """


class ServerError(APIError):
    """Raised on ``5xx``. Usually transient; the default transport retries these (see `IonQClient`)."""


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
    """Raise the `APIError` subclass matching an HTTP error status; a no-op below 400.

    5xx raises `ServerError`; any other unmapped 4xx raises `APIError`.
    """
    if status_code < 400:
        return
    exc_cls = _STATUS_TO_EXCEPTION.get(status_code, ServerError if status_code >= 500 else APIError)
    raise exc_cls(status_code, body, message, retry_after, request_id=request_id)
