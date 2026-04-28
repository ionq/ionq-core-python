# ionq-core

Python client for the IonQ Quantum Cloud Platform API.

[![PyPI](https://img.shields.io/pypi/v/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![Python versions](https://img.shields.io/pypi/pyversions/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-ionq.github.io-blue.svg)](https://ionq.github.io/ionq-core-python/)

`ionq-core` is a typed, async-capable Python client for the [IonQ Quantum Cloud Platform](https://ionq.com) REST API. It covers job submission and lifecycle, results retrieval, backend characterizations, sessions, and usage reporting. The HTTP layer is generated from IonQ's OpenAPI specification with [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client); a small set of hand-written extensions wraps it with retries, polling, pagination, structured exceptions, and an extension API for downstream SDKs.

The full API reference for this package is published at [ionq.github.io/ionq-core-python](https://ionq.github.io/ionq-core-python/).

## Looking for a higher-level interface?

`ionq-core` is the low-level HTTP client. Most users should pick the integration that matches their existing stack:

- **Qiskit** users -> [`qiskit-ionq`](https://pypi.org/project/qiskit-ionq/)
- **Cirq** users -> [`cirq-ionq`](https://pypi.org/project/cirq-ionq/)
- **PennyLane** users -> [`pennylane-ionq`](https://pypi.org/project/pennylane-ionq/)
- **CUDA-Q** users -> IonQ is configured as a backend in [NVIDIA CUDA-Q](https://github.com/NVIDIA/cuda-quantum/blob/main/runtime/cudaq/platform/default/rest/helpers/ionq/IonQServerHelper.cpp).
- **Multi-vendor users** -> IonQ is reachable via [`qbraid`](https://pypi.org/project/qbraid/).

Use this package directly if you want programmatic access to the IonQ REST API close to the wire, or if you are building a downstream SDK on top of it.

## Installation

```sh
pip install ionq-core
```

Requires Python 3.12 or newer.

## Quickstart

Submit a Bell-state circuit on the cloud simulator and read the result probabilities:

```python
from ionq_core import IonQClient, wait_for_job
from ionq_core.api.default import create_job, get_job_probabilities
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

client = IonQClient()  # reads IONQ_API_KEY from the environment

body = CircuitJobCreationPayload.from_dict({
    "type": "ionq.circuit.v1",
    "backend": "simulator",
    "shots": 100,
    "input": {
        "gateset": "qis",
        "circuit": [
            {"gate": "h", "targets": [0]},
            {"gate": "cnot", "control": 0, "target": 1},
        ],
    },
})

job = create_job.sync(client=client, body=body)
completed = wait_for_job(client, job.id, timeout=120)
probs = get_job_probabilities.sync(uuid=job.id, client=client)
print(probs.additional_properties)
```

Each generated endpoint module exposes four callables: `sync`, `sync_detailed`, `asyncio`, and `asyncio_detailed`. The `sync` and `asyncio` variants return the parsed body; the `_detailed` variants return a `Response[T]` with the status code, headers, and parsed body.

## Authentication

Authentication uses an API key passed as `Authorization: apiKey <key>` (note the `apiKey` prefix, not `Bearer`). `IonQClient` reads the key from the `IONQ_API_KEY` environment variable by default:

```sh
export IONQ_API_KEY="your-api-key"
```

```python
from ionq_core import IonQClient

client = IonQClient()                                       # IONQ_API_KEY from env
client = IonQClient(api_key="your-key")                     # explicit
client = IonQClient(base_url="https://api.ionq.co/v0.4")    # default base URL
```

If neither argument nor environment variable is set, `IonQClient()` raises `ValueError`. API keys are issued from your IonQ account.

## Async usage

Every endpoint exposes `asyncio` and `asyncio_detailed` callables alongside the synchronous variants. `IonQClient` itself supports both `with` and `async with`:

```python
import asyncio
from ionq_core import IonQClient
from ionq_core.api.backends import get_backends

async def main():
    async with IonQClient() as client:
        backends = await get_backends.asyncio(client=client)
        print([b.backend for b in backends])

asyncio.run(main())
```

The client opens both sync and async httpx transports during construction, so the same `client` instance can be used from both code paths.

## Handling errors

All exceptions inherit from `IonQError`. Concrete subclasses map to HTTP statuses and transport failures:

```text
IonQError
├── APIConnectionError        # network / DNS / TLS failures
│   └── APITimeoutError       # request timed out
└── APIError                  # 4xx / 5xx HTTP responses
    ├── BadRequestError       # 400
    ├── AuthenticationError   # 401
    ├── PermissionDeniedError # 403
    ├── NotFoundError         # 404
    ├── RateLimitError        # 429 (carries retry_after)
    └── ServerError           # 5xx
```

```python
from ionq_core import AuthenticationError, RateLimitError
from ionq_core.api.default import create_job

try:
    job = create_job.sync(client=client, body=payload)
except AuthenticationError as e:
    print(f"Invalid API key (request {e.request_id})")
except RateLimitError as e:
    print(f"Rate limited; retry after {e.retry_after}s")
```

Every `APIError` carries `status_code`, `body` (parsed JSON or raw string), `message`, and `request_id` from the `x-request-id` response header. Include `request_id` when contacting IonQ support about a specific failure.

## Retries and timeouts

Transient failures are retried automatically. The default policy is 2 retries on `429`, `500`, `502`, `503`, and `520`-`529`, with exponential backoff (factor 0.5, jitter 0.5, capped at 60 seconds). `Retry-After` headers are honored. The default request timeout is 60 seconds with a 10-second connect timeout.

```python
import httpx
from ionq_core import IonQClient

client = IonQClient(
    max_retries=5,
    timeout=httpx.Timeout(30.0, connect=10.0),
)
```

Set `max_retries=0` to disable retries entirely.

## Pagination

List endpoints return cursor-paginated responses. `iter_jobs`, `aiter_jobs`, `iter_session_jobs`, and `aiter_session_jobs` follow the cursor automatically and yield individual job objects:

```python
from itertools import islice
from ionq_core import iter_jobs

for job in islice(iter_jobs(client, status="completed"), 100):
    print(job.id, job.backend)
```

Each helper accepts the same filters as the underlying `get_jobs` / `get_session_jobs` endpoints (`status`, `target`, `session_id`, `submitter_id`, `limit`).

## Polling for job completion

`wait_for_job` polls a job until it reaches a terminal state (`completed`, `failed`, or `canceled`) or the timeout elapses. Polling starts at 1 second and grows by 1.5x to a 30-second cap; the default total timeout is 300 seconds.

```python
from ionq_core import wait_for_job, JobTimeoutError, JobFailedError

try:
    job = wait_for_job(client, job_id, timeout=300)
except JobTimeoutError as e:
    print(f"Polling timed out (last status: {e.last_status})")
except JobFailedError as e:
    print(f"Job failed: {e.failure}")
```

Pass `raise_on_failure=False` to receive the failed-job object instead of an exception. The async equivalent is `async_wait_for_job`.

## Sessions

`SessionManager` owns a long-running IonQ QPU session, optionally with limits on jobs, time (in minutes), or cost (in USD):

```python
from ionq_core import SessionManager

with SessionManager(client, "qpu.aria-1", max_jobs=10, max_time=60) as session:
    print(session.session_id)
    print(session.status())  # "started"
    # submit jobs against session.session_id ...
# the session is ended automatically on exit
```

`SessionManager.from_id(client, session_id)` reconnects to an existing session. The async path uses `async with` and `async_status()`.

## Advanced

### Logging and request hooks

`ClientExtension` bundles hooks, headers, and transport overrides. The `EventHook` and `AsyncEventHook` protocols receive each request and response, and may opt into `on_error`:

```python
import httpx
from ionq_core import IonQClient, ClientExtension, EventHook

class LoggingHook(EventHook):
    def on_request(self, request: httpx.Request) -> None:
        print(f">>> {request.method} {request.url}")

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        print(f"<<< {response.status_code} {request.url}")

client = IonQClient(extension=ClientExtension(event_hooks=(LoggingHook(),)))
```

Hook exceptions are logged and suppressed by default. Set `debug_hooks=True` on `ClientExtension` to re-raise them.

### Custom HTTP client

For unusual deployments (proxies, custom CA bundles, mTLS), pass `httpx_args` through `IonQClient` or attach your own `httpx.Client` to the returned client:

```python
import httpx

custom = httpx.Client(verify="/path/to/ca-bundle.pem")
client.set_httpx_client(custom)
```

For programmatic transport composition (caching, tracing, request signing), set `ClientExtension.transport_wrapper` and `async_transport_wrapper` to wrap the default retry transport.

### Mapping errors for downstream SDKs

`ClientExtension.error_mapper` lets a downstream SDK translate raised exceptions without losing the original chain:

```python
def map_error(exc: Exception) -> Exception:
    if isinstance(exc, RateLimitError):
        return MyDownstreamRateLimit(str(exc))
    return exc

client = IonQClient(extension=ClientExtension(error_mapper=map_error))
```

### Native trapped-ion gates

`gpi_matrix`, `gpi2_matrix`, `ms_matrix`, and `zz_matrix` return unitary matrices for IonQ's native gates as plain Python nested tuples (no NumPy dependency). Phase parameters are in turns (fractions of 2*pi); interaction angles are in units of pi.

```python
from ionq_core import gpi_matrix, ms_matrix

gpi_matrix(0.0)        # Pauli X
ms_matrix(0.0, 0.0)    # maximally-entangling Molmer-Sorensen gate
```

## SDK version vs API spec version

| `ionq-core` | IonQ REST API | Status  |
| ----------- | ------------- | ------- |
| 0.1.x       | v0.4          | Current |

The SDK version follows its own [SemVer 2.0](https://semver.org/spec/v2.0.0.html) cadence, independent of the upstream REST API version. Override the API version with `IonQClient(base_url=...)`.

## Versioning

This package follows [SemVer](https://semver.org/spec/v2.0.0.html), with three carve-outs that may ship in minor releases:

1. Changes that affect static types only, without changing runtime behavior.
2. Changes to library internals that are technically importable but not documented for external use (anything beginning with an underscore, or absent from the API reference).
3. Changes that we do not expect to impact the vast majority of users in practice.

Print the installed version with:

```python
import ionq_core
print(ionq_core.__version__)
```

The full release history is in [CHANGELOG.md](CHANGELOG.md).

## Requirements

- Python 3.12, 3.13, or 3.14
- `httpx >= 0.27, < 0.29`
- `httpx-retries >= 0.5`
- `attrs >= 24.2`
- `python-dateutil >= 2.9`

## Contributing

Most of `ionq_core/` is generated from the OpenAPI spec; pull requests touching files under `ionq_core/api/`, `ionq_core/models/`, or the generated `client.py`, `errors.py`, and `types.py` will be overwritten on the next regeneration. Hand-written extensions, tests, and docs accept contributions freely.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, the regeneration command, the 100% branch-coverage gate on hand-written code, and CLA details.

## Support

- Bug reports and feature requests: [GitHub Issues](https://github.com/ionq/ionq-core-python/issues)
- Security disclosures: see [SECURITY.md](SECURITY.md)
- Account, billing, or hardware-access questions: [ionq.com/contact](https://ionq.com/contact)

## License

Apache License 2.0. See [LICENSE](LICENSE).
