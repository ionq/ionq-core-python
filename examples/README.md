# ionq-core Examples

## Hamiltonian Energy Optimization

`hamiltonian_energy_optimization.py` demonstrates a Hamiltonian-energy Quantum Function using only the public `ionq-core` API:

- `IonQClient`
- `create_job.sync`
- `wait_for_job`
- typed models under `ionq_core.models`

It minimizes the one-qubit Hamiltonian `H = -Z` with a parameterized OpenQASM 3 `RY(theta)` ansatz and a small dependency-free coordinate search optimizer.

```sh
pip install ionq-core
export IONQ_API_KEY=...
python examples/hamiltonian_energy_optimization.py --iterations 4
```

The script targets the free `simulator` backend by default and prints each optimization iteration plus the final energy and parameters.
