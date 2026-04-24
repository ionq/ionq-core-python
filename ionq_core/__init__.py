# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""A Python client library for the [IonQ Cloud Platform API](https://docs.ionq.com/).

Provides full access to IonQ's quantum computing services with typed models for all
request and response objects. Supports both synchronous and asynchronous usage.

## Quick start

```python
from ionq_core import IonQClient
from ionq_core.api.backends import get_backends

# Authenticate with the IONQ_API_KEY environment variable
client = IonQClient()

# List available quantum backends
for backend in get_backends.sync(client=client):
    print(f"{backend.backend}: {backend.status}")
```

## Authentication

Get an API key from the [IonQ Cloud Console](https://cloud.ionq.com), then
either set the ``IONQ_API_KEY`` environment variable or pass it directly:

```python
client = IonQClient()  # reads IONQ_API_KEY
client = IonQClient(api_key="your-key")  # explicit key
```

## Submitting a job

```python
from ionq_core.api.default import create_job
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

job = create_job.sync(
    client=client,
    body=CircuitJobCreationPayload.from_dict(
        {
            "type": "ionq.circuit.v1",
            "backend": "simulator",
            "shots": 1000,
            "input": {
                "gateset": "qis",
                "circuit": [
                    {"gate": "h", "targets": [0]},
                    {"gate": "cnot", "targets": [0], "controls": [1]},
                ],
            },
        }
    ),
)
```

## Key features

- **Sync and async** - every endpoint has ``.sync()`` and ``.asyncio()`` variants.
- **Automatic retries** - transient errors (429, 5xx) are retried with exponential
  backoff. See `IonQClient` for configuration.
- **Typed exceptions** - HTTP errors are raised as `AuthenticationError`,
  `RateLimitError`, `ServerError`, etc. See `_exceptions` for the full hierarchy.
- **Pagination helpers** - `iter_jobs` and `aiter_jobs` follow cursors automatically.
- **Job polling** - `wait_for_job` and `async_wait_for_job` poll until completion.
- **Session management** - `SessionManager` wraps the session lifecycle as a
  context manager.
- **Native gate matrices** - `gpi_matrix`, `gpi2_matrix`, `ms_matrix`, and
  `zz_matrix` return pure-Python unitary matrices for simulation and verification.
- **Extensibility** - `ClientExtension` lets downstream SDKs inject hooks, headers,
  custom transports, and error mappers without modifying this library.
"""

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
