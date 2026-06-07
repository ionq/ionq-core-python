# ionq-core

A client library for accessing IonQ Cloud Platform API.

[![PyPI](https://img.shields.io/pypi/v/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![Python versions](https://img.shields.io/pypi/pyversions/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ionq/ionq-core-python/blob/main/LICENSE)
[![CI](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-ionq.github.io-blue.svg)](https://ionq.github.io/ionq-core-python/)

`ionq-core` is a typed, async-capable Python client for the [IonQ Cloud Platform](https://ionq.com) REST API. The HTTP layer is generated from IonQ's OpenAPI specification with [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client); a small set of hand-written extensions wraps it with retries, polling, pagination, structured exceptions, and an extension API for downstream SDKs.

The full API reference is published at [ionq.github.io/ionq-core-python](https://ionq.github.io/ionq-core-python/).

## Looking for a higher-level interface?

`ionq-core` is the low-level HTTP client. Most users should pick the integration that matches their existing stack:

- **Qiskit** users -> [`qiskit-ionq`](https://pypi.org/project/qiskit-ionq/)
- **Cirq** users -> [`cirq-ionq`](https://pypi.org/project/cirq-ionq/)
- **PennyLane** users -> [`pennylane-ionq`](https://pypi.org/project/pennylane-ionq/)
- **CUDA-Q** users -> IonQ is configured as a backend in [NVIDIA CUDA-Q](https://github.com/NVIDIA/cuda-quantum).
- **Multi-vendor users** -> IonQ is reachable via [`qbraid`](https://pypi.org/project/qbraid/).

Use this package directly if you want programmatic access to the IonQ REST API close to the wire, or if you are building a downstream SDK on top of it.

## Installation

```sh
pip install ionq-core
```

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
        "qubits": 2,
        "circuit": [
            {"gate": "h", "target": 0},
            {"gate": "cnot", "control": 0, "target": 1},
        ],
    },
})

job = create_job.sync(client=client, body=body)
completed = wait_for_job(client, job.id)
probs = get_job_probabilities.sync(uuid=job.id, client=client)
print(probs.additional_properties)
```

Each generated endpoint module exposes four callables: `sync`, `sync_detailed`, `asyncio`, and `asyncio_detailed`. The `sync` and `asyncio` variants return the parsed body; the `_detailed` variants return a `Response[T]` with the status code, headers, and parsed body.

## Examples

See [examples/](examples/README.md) for sync and async downstream-SDK integration examples using the extension API.

For options (`api_key`, `base_url`, `max_retries`, `timeout`, `extension`), error classes, retry behavior, pagination, polling, sessions, and downstream-SDK extension hooks, see the [API reference](https://ionq.github.io/ionq-core-python/).

## Versioning

This package follows [SemVer 2.0](https://semver.org/spec/v2.0.0.html), independent of the upstream REST API version - pass an explicit `base_url` to `IonQClient` to pin against a different API. Print the installed version with:

```python
import ionq_core
print(ionq_core.__version__)
```

The full release history is in [CHANGELOG.md](https://github.com/ionq/ionq-core-python/blob/main/CHANGELOG.md).

## Contributing

Most of `ionq_core/` is generated from the OpenAPI spec and overwritten on every regeneration. See [CONTRIBUTING.md](https://github.com/ionq/ionq-core-python/blob/main/CONTRIBUTING.md) for the boundary between generated and hand-written code, development setup, and the regeneration command.

## Support

- Bug reports and feature requests: [GitHub Issues](https://github.com/ionq/ionq-core-python/issues)
- Security disclosures: see [SECURITY.md](https://github.com/ionq/ionq-core-python/blob/main/SECURITY.md)
- Account, billing, or hardware-access questions: [ionq.com/contact](https://ionq.com/contact)

## License

Apache License 2.0. See [LICENSE](https://github.com/ionq/ionq-core-python/blob/main/LICENSE).
