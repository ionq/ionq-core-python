# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0


"""A client library for accessing IonQ Cloud Platform API"""

from .client import AuthenticatedClient, Client
from .exceptions import (
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
from .extensions import AsyncEventHook, ClientExtension, EventHook
from .gates import gpi2_matrix, gpi_matrix, ms_matrix, zz_matrix
from .ionq_client import IonQClient, __version__
from .pagination import aiter_jobs, aiter_session_jobs, iter_jobs, iter_session_jobs
from .polling import JobFailedError, JobTimeoutError, async_wait_for_job, wait_for_job
from .session import SessionManager
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
    "exceptions",
    "extensions",
    "gates",
    "gpi2_matrix",
    "gpi_matrix",
    "ionq_client",
    "iter_jobs",
    "iter_session_jobs",
    "ms_matrix",
    "pagination",
    "polling",
    "session",
    "wait_for_job",
    "zz_matrix",
)
