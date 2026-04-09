"""A client library for accessing IonQ Cloud Platform API"""

from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    IonQError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
)
from .client import AuthenticatedClient, Client
from .ionq_client import IonQClient, __version__

__all__ = (
    "APIConnectionError",
    "APIError",
    "APITimeoutError",
    "AuthenticatedClient",
    "AuthenticationError",
    "BadRequestError",
    "Client",
    "IonQClient",
    "IonQError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "__version__",
)
