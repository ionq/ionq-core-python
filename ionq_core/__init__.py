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
from ._extensions import AsyncEventHook, ClientExtension, EventHook
from ._gates import gpi2_matrix, gpi_matrix, ms_matrix, zz_matrix
from ._pagination import aiter_jobs, aiter_session_jobs, iter_jobs, iter_session_jobs
from ._polling import (
    JobFailedError,
    JobTimeoutError,
    async_wait_for_job,
    wait_for_job,
)
from ._session import SessionManager
from .client import AuthenticatedClient, Client
from .ionq_client import IonQClient, __version__
from .types import UNSET, Unset

__all__ = (
    "UNSET",
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
    "Unset",
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
