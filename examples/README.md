# Examples

Runnable scripts that exercise `ionq-core` against the live IonQ API.

## Hamiltonian-energy VQE

[`hamiltonian_energy_vqe.py`](hamiltonian_energy_vqe.py) builds a Hamiltonian Energy
Quantum Function with typed `ionq_core.models`, submits each evaluation via
`create_job`, polls with `wait_for_job`, and minimizes the energy with a
dependency-free SPSA optimizer.

| Component | Choice |
| --------- | ------ |
| Hamiltonian | H2 (STO-3G, r = 0.735 Å): `IZ`, `ZI`, `ZZ` (see note below) |
| Ansatz | Ry/Rz + CNOT + Ry/Rz (8 parameters, OpenQASM 3) |
| Optimizer | SPSA — two energy evaluations per iteration; keeps best seen |
| Backend | `simulator` (free tier) |

### Energy expectations

The script optimizes the **submitted** Pauli terms (`IZ`, `ZI`, `ZZ`). Two
details matter when comparing numbers:

1. **`II` term omitted** - the full H2 operator includes a constant `-0.0113` Ha
   identity shift. The API ignores `"II"` Pauli strings, so the script leaves it
   out and reports a shifted energy at the end.
2. **Shallow demo ansatz** - this is a small hardware-efficient circuit, not a
   full UCCSD ansatz. Expect the best submitted energy around **-0.15 to -0.25
   Ha** after SPSA, not the exact ground state.

| Quantity | Typical value |
| -------- | ------------- |
| Best energy (submitted terms) | ~ -0.15 to -0.25 Ha |
| + omitted `II` offset | add -0.0113 Ha |
| Exact ground state (reference) | ~ -1.137 Ha |

The exact reference is what a complete variational ansatz would target; this
example demonstrates the API loop, not state-of-the-art H2 convergence.

### Setup

```sh
pip install ionq-core
```

Get an API key from [cloud.ionq.com/settings/keys](https://cloud.ionq.com/settings/keys).

### Running

```sh
# Unix / macOS
export IONQ_API_KEY=your-api-key
python examples/hamiltonian_energy_vqe.py
```

```powershell
# Windows PowerShell
$env:IONQ_API_KEY = "your-api-key"
python examples/hamiltonian_energy_vqe.py
```

From a clone of this repository (with dev tools installed):

```sh
uv run python examples/hamiltonian_energy_vqe.py
```

The script prints each job submission, per-iteration SPSA progress (`E+` / `E−`),
the best energy on the submitted Hamiltonian, a shifted total that adds the
omitted `II` offset back, and the exact reference. Swap SPSA for `scipy.optimize` or
another method if you prefer — keep extra dependencies example-only
(`pip install scipy`), not in the core package.
