# Examples

These examples show direct `ionq-core` usage close to the IonQ REST API.

## Hamiltonian Energy Optimization

`hamiltonian_energy_optimization.py` builds a Hamiltonian Energy Quantum
Function with typed `ionq_core.models`, submits each energy evaluation with
`create_job`, waits with `wait_for_job`, and minimizes the returned energy with
a small dependency-free coordinate-search optimizer.

The example uses:

- Hamiltonian: `-ZI - IZ + 0.5 XX`
- Ansatz: a two-parameter OpenQASM 3 circuit
- Backend: `simulator`
- Optimizer: local coordinate search

Install and run:

```sh
pip install ionq-core
export IONQ_API_KEY=your-api-key
python examples/hamiltonian_energy_optimization.py
```

On Windows PowerShell, set the API key with:

```powershell
$env:IONQ_API_KEY = "your-api-key"
python examples/hamiltonian_energy_optimization.py
```

The script prints each submitted job id, the returned energy, and the best
parameters found so far.
