# ionq-core

[![PyPI version](https://img.shields.io/pypi/v/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A Python client library for the [IonQ Cloud Platform API](https://docs.ionq.com/), providing full access to IonQ's quantum computing services. Supports both synchronous and asynchronous usage, with typed models for all request and response objects.

Auto-generated from the [IonQ OpenAPI specification](https://docs.ionq.com/api-reference/v0.4/introduction) using [openapi-python-client](https://github.com/openapi-generators/openapi-python-client).

## Installation

```sh
pip install ionq-core
```

Requires Python 3.12+.

## Usage

```python
from ionq_core import IonQClient
from ionq_core.api.backends import get_backends
from ionq_core.api.default import create_job
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

# Uses IONQ_API_KEY env var by default
client = IonQClient()

# List available backends
backends = get_backends.sync(client=client)
for backend in backends:
    print(f"{backend.backend}: {backend.status} ({backend.qubits} qubits)")

# Submit a quantum circuit
job = create_job.sync(
    client=client,
    body=CircuitJobCreationPayload.from_dict({
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
    }),
)
print(f"Job submitted: {job.id} (status: {job.status})")
```

## Authentication

IonQ uses API key authentication. Get your key from the [IonQ Cloud Console](https://cloud.ionq.com).

```python
from ionq_core import IonQClient

# Option 1: Set the IONQ_API_KEY environment variable (recommended)
client = IonQClient()

# Option 2: Pass the key directly
client = IonQClient(api_key="your-api-key")

# Option 3: Use AuthenticatedClient for full control
from ionq_core import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://api.ionq.co/v0.4",
    token="your-api-key",
    prefix="apiKey",
    auth_header_name="Authorization",
)
```

Some endpoints (e.g., listing backends) do not require authentication. Use `Client` for those:

```python
from ionq_core import Client

client = Client(base_url="https://api.ionq.co/v0.4")
```

## Async usage

Every endpoint has both sync and async variants:

```python
import asyncio
from ionq_core import IonQClient
from ionq_core.api.backends import get_backends


async def main():
    client = IonQClient()
    backends = await get_backends.asyncio(client=client)
    for backend in backends:
        print(f"{backend.backend}: {backend.status}")


asyncio.run(main())
```

Both client types support context managers for proper connection cleanup:

```python
async with IonQClient() as client:
    backends = await get_backends.asyncio(client=client)
```

## Handling errors

The client raises typed exceptions for all HTTP error responses:

```python
from ionq_core import IonQClient, RateLimitError, AuthenticationError, ServerError

client = IonQClient()

try:
    job = create_job.sync(client=client, body=payload)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except ServerError as e:
    print(f"Server error: {e.status_code}")
```

| Status code | Exception |
|---|---|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 429 | `RateLimitError` |
| 5xx | `ServerError` |

All exceptions inherit from `APIError`, which inherits from `IonQError`. Connection failures raise `APIConnectionError`; timeouts raise `APITimeoutError`.

## Retries

The client automatically retries transient errors (429, 500, 502, 503, 520-529) and connection/timeout failures with exponential backoff. Default: 2 retries.

```python
client = IonQClient(max_retries=5)  # more retries
client = IonQClient(max_retries=0)  # disable retries
```

`Retry-After` headers on 429 responses are respected.

## Pagination

Endpoints that return paginated results have auto-pagination helpers:

```python
from ionq_core import IonQClient, iter_jobs

client = IonQClient()
for job in iter_jobs(client, status="completed"):
    print(job.id)
```

Async:

```python
from ionq_core import aiter_jobs

async for job in aiter_jobs(client):
    print(job.id)
```

Also available: `iter_session_jobs` / `aiter_session_jobs`.

## Waiting for job completion

```python
from ionq_core import IonQClient, wait_for_job

client = IonQClient()
job = create_job.sync(client=client, body=payload)
completed_job = wait_for_job(client, job.id, timeout=300)
print(completed_job.status)  # "completed"
```

Polls with exponential backoff (1s initial, 30s max). Raises `JobTimeoutError` on timeout, `JobFailedError` if the job fails. Async: `async_wait_for_job`.

## Native gate matrices

Pure-Python unitary matrices for IonQ's native trapped-ion gates, useful for simulation and verification:

```python
from ionq_core import gpi_matrix, gpi2_matrix, ms_matrix, zz_matrix

# Phase parameters (phi) are in turns (fractions of 2*pi)
# Interaction parameters (angle) are in units of pi
gpi_matrix(0)       # 2x2 Pauli X
gpi2_matrix(0.25)   # 2x2 pi/2 rotation
ms_matrix(0, 0)     # 4x4 maximally-entangling MS gate (angle defaults to 0.25)
zz_matrix(0.1)      # 4x4 ZZ interaction
```

Matrices are returned as nested tuples of complex numbers (no numpy dependency).

## Session management

`SessionManager` provides a context manager for IonQ priority sessions:

```python
from ionq_core import IonQClient, SessionManager

client = IonQClient()

with SessionManager(client, "qpu.aria-1", max_jobs=10, max_time=60) as session:
    # submit jobs using session.session_id
    print(session.session_id)
    print(session.status())

# Reconnect to an existing session
session = SessionManager.from_id(client, "existing-session-id")
```

## Available endpoints

### Backends

| Function | Module | Auth |
|---|---|---|
| List backends | `ionq_core.api.backends.get_backends` | No |
| Get a backend | `ionq_core.api.backends.get_backend` | No |

### Characterizations

| Function | Module | Auth |
|---|---|---|
| List characterizations | `ionq_core.api.characterizations.get_characterizations_for_backend` | No |
| Get a characterization | `ionq_core.api.characterizations.get_characterization` | Yes |

### Jobs

| Function | Module | Auth |
|---|---|---|
| Create a job | `ionq_core.api.default.create_job` | Yes |
| List jobs | `ionq_core.api.default.get_jobs` | Yes |
| Get a job | `ionq_core.api.default.get_job` | Yes |
| Delete a job | `ionq_core.api.default.delete_job` | Yes |
| Delete jobs (bulk) | `ionq_core.api.default.delete_jobs` | Yes |
| Cancel a job | `ionq_core.api.default.cancel_job` | Yes |
| Cancel jobs (bulk) | `ionq_core.api.default.cancel_jobs` | Yes |
| Get job cost | `ionq_core.api.default.get_job_cost` | Yes |
| Estimate job cost | `ionq_core.api.default.estimate_job_cost` | Yes |

### Sessions

| Function | Module | Auth |
|---|---|---|
| Create a session | `ionq_core.api.default.create_session` | Yes |
| List sessions | `ionq_core.api.default.get_sessions` | Yes |
| Get a session | `ionq_core.api.default.get_session` | Yes |
| End a session | `ionq_core.api.default.end_session` | Yes |
| List session jobs | `ionq_core.api.default.get_session_jobs` | Yes |

### Other

| Function | Module | Auth |
|---|---|---|
| Who am I | `ionq_core.api.whoami.get_whoami` | Yes |
| Get usage | `ionq_core.api.usage.get_usages` | Yes |

Each endpoint module provides four functions:

- **`sync`** - synchronous call, returns the parsed response
- **`asyncio`** - async call, returns the parsed response
- **`sync_detailed`** - synchronous call, returns `Response[T]` with status code, headers, and parsed body
- **`asyncio_detailed`** - async call, returns `Response[T]` with status code, headers, and parsed body

## Models

All request and response bodies are typed as [attrs](https://www.attrs.org/) classes with `from_dict()` and `to_dict()` methods:

```python
from ionq_core.models.backend import Backend

# Deserialize from API response dict
backend = Backend.from_dict({"backend": "qpu.aria-1", "status": "available", ...})

# Access typed attributes
print(backend.backend)  # "qpu.aria-1"
print(backend.qubits)   # 25

# Serialize back to dict
data = backend.to_dict()
```

Optional fields use the `Unset` sentinel (not `None`) to distinguish between "not provided" and "explicitly null":

```python
from ionq_core.types import UNSET, Unset

if not isinstance(backend.characterization_id, Unset):
    print(f"Characterization: {backend.characterization_id}")
```

## Advanced

### Timeouts

```python
import httpx
from ionq_core import IonQClient

client = IonQClient(timeout=httpx.Timeout(30.0, connect=10.0))
```

### Custom headers

```python
client = IonQClient().with_headers({"X-Custom-Header": "value"})
```

### Custom HTTP client

For full control over the HTTP layer, inject your own `httpx.Client`:

```python
import httpx
from ionq_core import IonQClient

custom_httpx = httpx.Client(
    base_url="https://api.ionq.co/v0.4",
    headers={"Authorization": "apiKey your-key"},
    timeout=60.0,
)

client = IonQClient(api_key="your-key")
client.set_httpx_client(custom_httpx)
```

### Accessing raw responses

Use the `_detailed` variants to get status codes and headers:

```python
from ionq_core.api.whoami import get_whoami

response = get_whoami.sync_detailed(client=client)
print(response.status_code)  # HTTPStatus.OK
print(response.headers)  # dict of response headers
print(response.parsed)  # Whoami object
print(response.content)  # raw bytes
```

## Regenerating the client

The client is generated from the vendored OpenAPI spec. To regenerate after API changes:

```sh
# Fetch the latest spec
curl -s https://api-staging.ionq.co/v0.4/api-docs -o openapi.json

# Apply overlay if present (patches spec issues that the generator can't handle)
if [ -f openapi-overlay.yaml ]; then
    uvx oas-patch==0.6.0 overlay openapi.json openapi-overlay.yaml -o /tmp/patched-spec.json
else
    cp openapi.json /tmp/patched-spec.json
fi

# Regenerate (custom template preserves hand-written __init__.py exports)
uvx openapi-python-client==0.28.3 generate \
    --path /tmp/patched-spec.json \
    --meta none \
    --config openapi-python-client-config.yaml \
    --custom-template-path custom-templates \
    --output-path ionq_core \
    --overwrite
```

### OpenAPI Overlay

If the upstream spec contains patterns that the code generator cannot handle, fixes are applied via an [OpenAPI Overlay](https://spec.openapis.org/overlay/v1.1.0.html) file (`openapi-overlay.yaml`) using [oas-patch](https://pypi.org/project/oas-patch/). The overlay is declarative, version-controlled, and applied automatically during generation. The vendored `openapi.json` is always the unmodified upstream spec. When the upstream issue is resolved, delete the corresponding action from the overlay (or the entire file) and the pipeline continues to work without it.

## Development

```sh
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run ruff check          # Lint
uv run ruff format --check # Check formatting
uv run ty check ionq_core/ # Type check
```

## Publishing

Publishing is handled automatically via trusted publishing on tagged releases:

```sh
git tag v0.1.0
git push origin v0.1.0
```

For a new build to be accepted at PyPi the version number in pyproject.toml must be incremented.

In principle you can also publish the package to PyPi manually using the uv package manager but the automatic approach is recommended.


## License

Apache-2.0. See [LICENSE](LICENSE) for details.
