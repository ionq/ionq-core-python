# Examples

Direct `ionq-core` examples that use the typed models close to the IonQ REST API.

## Hamiltonian Energy Optimization

[`hamiltonian_energy_optimization.py`](hamiltonian_energy_optimization.py) builds a
Hamiltonian Energy Quantum Function with the typed `ionq_core.models` payloads,
submits each energy evaluation via `create_job`, polls with `wait_for_job`, and
minimizes the energy using a dependency-free SPSA optimizer.

| Component   | Choice                                                                 |
| ----------- | ---------------------------------------------------------------------- |
| Hamiltonian | Two-qubit transverse-field Ising: `H = -ZZ - 0.5(XI + IX)`            |
| Ansatz      | Hardware-efficient Ry/Rz rotations + CNOT (4 parameters, OpenQASM 3)  |
| Optimizer   | SPSA — two energy evaluations per iteration regardless of param count |
| Backend     | `simulator` (free tier)                                                |

### Setup

```sh
pip install ionq-core
```

### Running

Set your API key and run the script:

```sh
# Unix / macOS
export IONQ_API_KEY=your-api-key
python examples/hamiltonian_energy_optimization.py
```

```powershell
# Windows PowerShell
$env:IONQ_API_KEY = "your-api-key"
python examples/hamiltonian_energy_optimization.py
```

The script prints each job submission, per-iteration SPSA progress, and the
final optimal parameters with the best energy found.