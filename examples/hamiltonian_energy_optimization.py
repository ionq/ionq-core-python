# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Optimize a Hamiltonian-energy quantum function on the IonQ simulator.

Demonstrates the end-to-end variational loop: build a typed Hamiltonian
Energy payload with ``ionq_core.models``, submit via ``create_job``, poll
with ``wait_for_job``, and minimize the energy with a client-side optimizer.

Hamiltonian
    Two-qubit transverse-field Ising model (TFIM):
    ``H = -J ZZ - h (XI + IX)``
    with ``J = 1.0`` and ``h = 0.5``.

Ansatz
    Hardware-efficient two-qubit OpenQASM 3 circuit with four parameters:
    ``Ry(θ0) Rz(θ1)`` on qubit 0, ``Ry(θ2) Rz(θ3)`` on qubit 1, followed
    by a CNOT entangling gate.

Optimizer
    SPSA (Simultaneous Perturbation Stochastic Approximation), implemented
    without external dependencies.  SPSA is well-suited to noisy quantum
    objectives because it estimates the gradient with only two function
    evaluations per iteration, regardless of parameter count.

Usage::

    pip install ionq-core
    export IONQ_API_KEY=your-api-key   # Unix / macOS
    python examples/hamiltonian_energy_optimization.py
"""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from ionq_core import IonQClient, wait_for_job
from ionq_core.api.default import create_job
from ionq_core.client import AuthenticatedClient
from ionq_core.models.ansatz import Ansatz
from ionq_core.models.get_job_response import GetJobResponse
from ionq_core.models.hamiltonian_energy_data import HamiltonianEnergyData
from ionq_core.models.hamiltonian_energy_input import HamiltonianEnergyInput
from ionq_core.models.hamiltonian_energy_input_data import HamiltonianEnergyInputData
from ionq_core.models.hamiltonian_pauli_term import HamiltonianPauliTerm
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.quantum_function_job_creation_payload import QuantumFunctionJobCreationPayload

# ---------------------------------------------------------------------------
# Problem definition
# ---------------------------------------------------------------------------

#: Two-qubit transverse-field Ising Hamiltonian: H = -ZZ - 0.5*(XI + IX)
HAMILTONIAN: list[HamiltonianPauliTerm] = [
    HamiltonianPauliTerm(pauli_string="ZZ", coefficient=-1.0),
    HamiltonianPauliTerm(pauli_string="XI", coefficient=-0.5),
    HamiltonianPauliTerm(pauli_string="IX", coefficient=-0.5),
]

#: Hardware-efficient ansatz — Ry/Rz single-qubit rotations + CNOT.
ANSATZ_QASM3 = """\
OPENQASM 3.0;
include "stdgates.inc";

input float theta0;
input float theta1;
input float theta2;
input float theta3;

qubit[2] q;

ry(theta0) q[0];
rz(theta1) q[0];
ry(theta2) q[1];
rz(theta3) q[1];
cx q[0], q[1];
"""

NUM_PARAMS = 4
INITIAL_PARAMS: list[float] = [random.uniform(0, 2 * math.pi) for _ in range(NUM_PARAMS)]


# ---------------------------------------------------------------------------
# Payload construction and job submission
# ---------------------------------------------------------------------------


def build_payload(
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
) -> QuantumFunctionJobCreationPayload:
    """Assemble a typed Hamiltonian Energy Quantum Function payload."""
    return QuantumFunctionJobCreationPayload(
        backend=backend,
        type_="quantum-function",
        name="hamiltonian-energy-optimization-example",
        shots=shots,
        input_=HamiltonianEnergyInput(
            data=HamiltonianEnergyInputData(
                type_="hamiltonian-energy",
                data=HamiltonianEnergyData(hamiltonian=HAMILTONIAN, ansatz=Ansatz(data=ANSATZ_QASM3)),
            ),
            params=list(params),
        ),
    )


def evaluate_energy(
    client: AuthenticatedClient,
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
    timeout: float = 300,
) -> tuple[str, float]:
    """Submit one energy-evaluation job and return ``(job_id, energy)``."""
    payload = build_payload(params, backend=backend, shots=shots)
    created = create_job.sync(client=client, body=payload)
    if not isinstance(created, JobCreationResponse):
        msg = f"Unexpected response from create_job: {created!r}"
        raise RuntimeError(msg)

    completed = wait_for_job(client, created.id, timeout=timeout)
    return created.id, _extract_energy(completed)


def _extract_energy(job: GetJobResponse) -> float:
    """Walk the job output to find a numeric energy value."""
    output = job.output.additional_properties
    for value in _find_energy_values(output):
        if isinstance(value, int | float):
            return float(value)
    msg = f"No numeric energy found in job output: {output!r}"
    raise ValueError(msg)


def _find_energy_values(data: Any) -> list[Any]:
    """Recursively search nested dicts for energy-like keys."""
    if not isinstance(data, Mapping):
        return [data]
    candidates: list[Any] = []
    for key in ("energy", "expectation", "expectation_value", "value", "minimum_value"):
        if key in data:
            candidates.append(data[key])
    for key in ("result", "results", "solution", "output"):
        if key in data:
            candidates.extend(_find_energy_values(data[key]))
    return candidates


# ---------------------------------------------------------------------------
# SPSA optimizer (dependency-free)
# ---------------------------------------------------------------------------


def spsa_minimize(
    objective: Callable[[Sequence[float]], float],
    initial_params: Sequence[float],
    *,
    maxiter: int = 20,
    learning_rate: float = 0.1,
    perturbation: float = 0.3,
    lr_decay: float = 0.602,
    pert_decay: float = 0.101,
    stability: float = 1.0,
) -> tuple[list[float], float]:
    """Minimize *objective* using SPSA.

    At each iteration the gradient is approximated with two objective
    evaluations using a random perturbation vector Δ drawn from
    {-1, +1}^n (Bernoulli ±1).  The gain sequences ``a_k`` and ``c_k``
    follow the standard SPSA schedule (Spall, 1998).

    Returns the best parameters and best energy found.
    """
    params = list(initial_params)
    best_params = params[:]
    best_energy = math.inf

    for k in range(1, maxiter + 1):
        a_k = learning_rate / (k + stability) ** lr_decay
        c_k = perturbation / k**pert_decay

        # Bernoulli ±1 perturbation vector
        delta = [random.choice((-1.0, 1.0)) for _ in params]

        params_plus = [p + c_k * d for p, d in zip(params, delta, strict=True)]
        params_minus = [p - c_k * d for p, d in zip(params, delta, strict=True)]

        energy_plus = objective(params_plus)
        energy_minus = objective(params_minus)

        # Approximate gradient and update
        for i in range(len(params)):
            g_i = (energy_plus - energy_minus) / (2 * c_k * delta[i])
            params[i] -= a_k * g_i

        # Track best
        current_energy = min(energy_plus, energy_minus)
        if current_energy < best_energy:
            best_energy = current_energy
            best_params = params_plus[:] if energy_plus <= energy_minus else params_minus[:]

        print(f"  iter {k:>3d}/{maxiter}  E+ = {energy_plus:+.6f}  E- = {energy_minus:+.6f}  best = {best_energy:+.6f}")

    return best_params, best_energy


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the Hamiltonian energy optimization example."""
    client = IonQClient(additional_user_agent="ionq-core-example/hamiltonian-energy")

    call_count = 0

    def objective(params: Sequence[float]) -> float:
        nonlocal call_count
        call_count += 1
        job_id, energy = evaluate_energy(client, params)
        print(f"  [eval {call_count}] job={job_id}  energy={energy:+.6f}  params={[round(p, 4) for p in params]}")
        return energy

    print("Hamiltonian: H = -ZZ - 0.5*(XI + IX)  (transverse-field Ising, 2 qubits)")
    print(f"Ansatz: Ry/Rz + CNOT  ({NUM_PARAMS} parameters)")
    print("Optimizer: SPSA  (20 iterations, 2 evals/iter)")
    print(f"Initial params: {[round(p, 4) for p in INITIAL_PARAMS]}")
    print()

    best_params, best_energy = spsa_minimize(objective, INITIAL_PARAMS, maxiter=20)

    print()
    print(f"Optimization complete  ({call_count} energy evaluations)")
    print(f"Best energy:  {best_energy:+.8f}")
    print(f"Best params:  {[round(p, 6) for p in best_params]}")

    # The exact ground-state energy for H = -ZZ - 0.5(XI+IX) is
    # the smallest eigenvalue ≈ -1.118.  With shot noise the optimizer
    # should approach this neighbourhood.
    sys.exit(0)


if __name__ == "__main__":
    main()