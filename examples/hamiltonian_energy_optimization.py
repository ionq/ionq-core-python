# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Optimize a Hamiltonian-energy quantum function with ionq-core.

This example uses a two-qubit OpenQASM 3 ansatz with two parameters, the
Hamiltonian ``-ZI - IZ + 0.5 XX``, and a dependency-free coordinate-search
optimizer. Each objective evaluation submits a Hamiltonian Energy Quantum
Function job to the free ``simulator`` backend and waits for completion.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
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

ANSATZ_OPENQASM = """OPENQASM 3.0;
include "stdgates.inc";

input float theta0;
input float theta1;
qubit[2] q;

ry(theta0) q[0];
ry(theta1) q[1];
cx q[0], q[1];
"""

INITIAL_PARAMETERS = (0.3, -0.2)
HAMILTONIAN = (
    HamiltonianPauliTerm(pauli_string="ZI", coefficient=-1.0),
    HamiltonianPauliTerm(pauli_string="IZ", coefficient=-1.0),
    HamiltonianPauliTerm(pauli_string="XX", coefficient=0.5),
)


@dataclass(frozen=True)
class OptimizationResult:
    """Best parameters and energy found by the local optimizer."""

    params: tuple[float, ...]
    energy: float


def build_hamiltonian_energy_payload(
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
) -> QuantumFunctionJobCreationPayload:
    """Build a typed Hamiltonian Energy Quantum Function payload."""
    hamiltonian_data = HamiltonianEnergyData(
        hamiltonian=list(HAMILTONIAN),
        ansatz=Ansatz(data=ANSATZ_OPENQASM),
    )
    return QuantumFunctionJobCreationPayload(
        backend=backend,
        type_="quantum-function",
        name="Hamiltonian energy optimization example",
        shots=shots,
        input_=HamiltonianEnergyInput(
            data=HamiltonianEnergyInputData(type_="hamiltonian-energy", data=hamiltonian_data),
            params=list(params),
        ),
    )


def submit_energy_job(
    client: AuthenticatedClient,
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
    timeout: float = 300,
) -> tuple[str, float]:
    """Submit one energy-evaluation job and return ``(job_id, energy)``."""
    payload = build_hamiltonian_energy_payload(params, backend=backend, shots=shots)
    created = create_job.sync(client=client, body=payload)
    if not isinstance(created, JobCreationResponse):
        raise RuntimeError("IonQ API did not return a job creation response")

    completed = wait_for_job(client, created.id, timeout=timeout)
    return created.id, extract_energy(completed)


def extract_energy(job: GetJobResponse) -> float:
    """Extract a numeric energy from a completed Quantum Function job response."""
    output = job.output.additional_properties
    for candidate in _energy_candidates(output):
        if isinstance(candidate, int | float):
            return float(candidate)
    raise ValueError(f"Could not find a numeric energy in job output: {output!r}")


def coordinate_search(
    objective: Callable[[Sequence[float]], float],
    initial_params: Sequence[float],
    *,
    iterations: int = 4,
    initial_step: float = 0.4,
) -> OptimizationResult:
    """Minimize ``objective`` with a small coordinate search."""
    params = list(initial_params)
    best_energy = objective(params)
    step = initial_step

    for iteration in range(1, iterations + 1):
        for axis in range(len(params)):
            best_candidate = params[:]
            for direction in (-1.0, 1.0):
                candidate = params[:]
                candidate[axis] += direction * step
                energy = objective(candidate)
                if energy < best_energy:
                    best_energy = energy
                    best_candidate = candidate
            params = best_candidate
        print(f"iteration={iteration} step={step:.3f} energy={best_energy:.8f} params={params}")
        step *= 0.5

    return OptimizationResult(params=tuple(params), energy=best_energy)


def _energy_candidates(value: Any) -> list[Any]:
    if not isinstance(value, Mapping):
        return [value]

    candidates: list[Any] = []
    for key in ("energy", "expectation", "expectation_value", "value", "minimum_value"):
        if key in value:
            candidates.append(value[key])
    for nested_key in ("result", "results", "solution", "output"):
        if nested_key in value:
            candidates.extend(_energy_candidates(value[nested_key]))
    return candidates


def main() -> None:
    """Run the example against the configured IonQ account."""
    client = IonQClient(additional_user_agent="ionq-core-example/hamiltonian-energy")

    def objective(params: Sequence[float]) -> float:
        job_id, energy = submit_energy_job(client, params)
        print(f"job_id={job_id} energy={energy:.8f} params={list(params)}")
        return energy

    result = coordinate_search(objective, INITIAL_PARAMETERS)
    print(f"best_energy={result.energy:.8f} best_params={list(result.params)}")


if __name__ == "__main__":
    main()
