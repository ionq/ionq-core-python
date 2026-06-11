# Examples

These examples use `ionq-core` directly against the IonQ Cloud Platform API.

## Setup

```sh
python -m pip install ionq-core
export IONQ_API_KEY=...
```

The client reads `IONQ_API_KEY` from the environment and sends it with IonQ's
`apiKey` authorization scheme.

## Hamiltonian energy quantum function

Run a small client-side optimization loop that submits Hamiltonian Energy
quantum-function jobs to the free `simulator` backend:

```sh
python examples/hamiltonian_energy_optimization.py
```

The example builds the quantum-function payload with the generated typed
models, submits each parameter vector with `create_job`, waits with
`wait_for_job`, and prints the per-iteration energy plus the final parameters.
