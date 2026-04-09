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
from ._pagination import aiter_jobs, aiter_session_jobs, iter_jobs, iter_session_jobs
from ._polling import (
    JobFailedError,
    JobTimeoutError,
    async_wait_for_job,
    wait_for_job,
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
    "JobFailedError",
    "JobTimeoutError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "__version__",
    "aiter_jobs",
    "aiter_session_jobs",
    "async_wait_for_job",
    "iter_jobs",
    "iter_session_jobs",
    "wait_for_job",
)
