# ionq-core

A typed, async-capable Python client for the [IonQ Cloud Platform](https://ionq.com) REST API.

[![PyPI](https://img.shields.io/pypi/v/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![Python versions](https://img.shields.io/pypi/pyversions/ionq-core.svg)](https://pypi.org/project/ionq-core/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ionq/ionq-core-python/blob/main/LICENSE)
[![CI](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ionq/ionq-core-python/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-ionq.github.io-blue.svg)](https://ionq.github.io/ionq-core-python/)

The HTTP layer is generated from IonQ's OpenAPI specification with [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client); hand-written extensions add retries, polling, pagination, structured exceptions, and an extension API for downstream SDKs.

## Higher-level interfaces

Most users should pick the integration matching their stack:

- **Qiskit** -> [`qiskit-ionq`](https://pypi.org/project/qiskit-ionq/)
- **Cirq** -> [`cirq-ionq`](https://pypi.org/project/cirq-ionq/)
- **PennyLane** -> [`pennylane-ionq`](https://pypi.org/project/pennylane-ionq/)
- **CUDA-Q** -> IonQ is a backend in [NVIDIA CUDA-Q](https://github.com/NVIDIA/cuda-quantum).
- **Multi-vendor** -> IonQ is reachable via [`qbraid`](https://pypi.org/project/qbraid/).

Use this package directly for REST access close to the wire, or to build a downstream SDK on top of it.

## Installation

```sh
pip install ionq-core
```

## Quickstart

Submit a Bell-state circuit to the cloud simulator and read its probabilities:

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

Each generated endpoint module exposes `sync`, `sync_detailed`, `asyncio`, and `asyncio_detailed`. The plain variants return the parsed body; the `_detailed` ones return a `Response[T]` with the status code, headers, and parsed body.

For client options, error classes, retries, pagination, polling, sessions, and extension hooks, see the [API reference](https://ionq.github.io/ionq-core-python/).

## Versioning

This package follows [SemVer 2.0](https://semver.org/spec/v2.0.0.html), independent of the upstream REST API version - pass an explicit `base_url` to `IonQClient` to pin against a different API. The installed version is `ionq_core.__version__`.

Release history: [CHANGELOG.md](https://github.com/ionq/ionq-core-python/blob/main/CHANGELOG.md).

## Contributing

Most of `ionq_core/` is generated from the OpenAPI spec and overwritten on every regeneration. [CONTRIBUTING.md](https://github.com/ionq/ionq-core-python/blob/main/CONTRIBUTING.md) covers the generated/hand-written boundary, development setup, and the regeneration command.

## Support

- Bugs and feature requests: [GitHub Issues](https://github.com/ionq/ionq-core-python/issues)
- Security disclosures: [SECURITY.md](https://github.com/ionq/ionq-core-python/blob/main/SECURITY.md)
- Account, billing, or hardware access: [ionq.com/contact](https://ionq.com/contact)

## License

Apache License 2.0. See [LICENSE](https://github.com/ionq/ionq-core-python/blob/main/LICENSE).
