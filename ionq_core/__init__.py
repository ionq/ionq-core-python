"""A client library for accessing IonQ Cloud Platform API"""

from ._gates import gpi2_matrix, gpi_matrix, ms_matrix, zz_matrix
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
from ._extensions import AsyncEventHook, ClientExtension, EventHook
from ._pagination import aiter_jobs, aiter_session_jobs, iter_jobs, iter_session_jobs
from ._session import SessionManager
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
    "AsyncEventHook",
    "AuthenticatedClient",
    "AuthenticationError",
    "BadRequestError",
    "Client",
    "ClientExtension",
    "EventHook",
    "IonQClient",
    "IonQError",
    "JobFailedError",
    "JobTimeoutError",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "SessionManager",
    "__version__",
    "aiter_jobs",
    "aiter_session_jobs",
    "async_wait_for_job",
    "gpi2_matrix",
    "gpi_matrix",
    "iter_jobs",
    "iter_session_jobs",
    "ms_matrix",
    "wait_for_job",
    "zz_matrix",
)
