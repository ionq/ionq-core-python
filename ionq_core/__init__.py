# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

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

from . import _exceptions, _extensions, _gates, _pagination, _polling, _session

__doc__ = "\n\n".join([
    "A client library for accessing IonQ Cloud Platform API",
    f"## Exceptions\n\n{_exceptions.__doc__}",
    f"## Extensions\n\n{_extensions.__doc__}",
    f"## Native Gates\n\n{_gates.__doc__}",
    f"## Job Polling\n\n{_polling.__doc__}",
    f"## Pagination\n\n{_pagination.__doc__}",
    f"## Sessions\n\n{_session.__doc__}",
])
