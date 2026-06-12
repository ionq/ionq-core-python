# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Hamiltonian-energy Quantum Function example with client-side optimization.

This example minimizes the one-qubit Hamiltonian ``H = -Z`` with a
parameterized OpenQASM 3 ansatz, ``RY(theta) |0>``. The optimizer is a small
dependency-free coordinate search that repeatedly submits Hamiltonian-energy
Quantum Function jobs through `ionq-core`.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from ionq_core import AuthenticatedClient, IonQClient, wait_for_job
from ionq_core.api.default import create_job
from ionq_core.models.ansatz import Ansatz
from ionq_core.models.hamiltonian_energy_data import HamiltonianEnergyData
from ionq_core.models.hamiltonian_energy_input import HamiltonianEnergyInput
from ionq_core.models.hamiltonian_energy_input_data import HamiltonianEnergyInputData
from ionq_core.models.hamiltonian_pauli_term import HamiltonianPauliTerm
from ionq_core.models.quantum_function_job_creation_payload import QuantumFunctionJobCreationPayload

ANSATZ_OPENQASM = """OPENQASM 3.0;
input float theta;
qubit[1] q;
ry(theta) q[0];
"""


@dataclass(frozen=True)
class OptimizationResult:
    """Result from the client-side coordinate-search loop."""

    parameters: list[float]
    energy: float
    history: list[tuple[int, list[float], float]]


def build_hamiltonian_energy_payload(
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
    name: str = "ionq-core hamiltonian energy example",
) -> QuantumFunctionJobCreationPayload:
    """Build a typed Hamiltonian-energy Quantum Function payload."""
    return QuantumFunctionJobCreationPayload(
        backend=backend,
        type_="quantum-function",
        input_=HamiltonianEnergyInput(
            data=HamiltonianEnergyInputData(
                type_="hamiltonian-energy",
                data=HamiltonianEnergyData(
                    hamiltonian=[HamiltonianPauliTerm(pauli_string="Z", coefficient=-1.0)],
                    ansatz=Ansatz(data=ANSATZ_OPENQASM),
                ),
            ),
            params=list(params),
        ),
        name=name,
        shots=shots,
    )


def evaluate_energy(
    client: AuthenticatedClient,
    params: Sequence[float],
    *,
    backend: str = "simulator",
    shots: int = 100,
    poll_interval: float = 1.0,
    timeout: float = 300.0,
    create_job_sync: Callable[..., Any] = create_job.sync,
    wait_for_job_fn: Callable[..., Any] = wait_for_job,
) -> float:
    """Submit a Hamiltonian-energy job and return its completed energy."""
    payload = build_hamiltonian_energy_payload(params, backend=backend, shots=shots)
    created = create_job_sync(client=client, body=payload)
    if created is None:
        raise RuntimeError("IonQ API did not return a job creation response")

    completed = wait_for_job_fn(client, created.id, poll_interval=poll_interval, timeout=timeout)
    return extract_energy(completed)


def extract_energy(completed_job: Any) -> float:
    """Extract an energy value from a completed Quantum Function job response."""
    output = completed_job.output.to_dict()
    candidates = [output.get("energy"), output.get("value")]

    result = output.get("result")
    if isinstance(result, dict):
        candidates.append(result.get("energy"))

    solution = output.get("solution")
    if isinstance(solution, dict):
        candidates.append(solution.get("minimum_value"))

    for candidate in candidates:
        if isinstance(candidate, (int, float)):
            return float(candidate)

    raise KeyError("completed job output did not contain an energy value")


def coordinate_search(
    energy_fn: Callable[[list[float]], float],
    initial_params: Sequence[float],
    *,
    step_size: float = 0.4,
    min_step: float = 0.025,
    max_iterations: int = 8,
    log: Callable[[str], None] = print,
) -> OptimizationResult:
    """Minimize ``energy_fn`` with a small deterministic coordinate search."""
    params = list(initial_params)
    energy = energy_fn(params)
    history = [(0, params.copy(), energy)]
    log(f"iteration 0: energy={energy:.12g}, params={params}")

    step = step_size
    for iteration in range(1, max_iterations + 1):
        improved = False

        for index in range(len(params)):
            for direction in (1.0, -1.0):
                candidate = params.copy()
                candidate[index] += direction * step
                candidate_energy = energy_fn(candidate)
                if candidate_energy < energy:
                    params = candidate
                    energy = candidate_energy
                    improved = True

        if improved:
            history.append((iteration, params.copy(), energy))
        else:
            step *= 0.5

        log(f"iteration {iteration}: energy={energy:.12g}, params={params}, step={step:.12g}")

        if not improved and step < min_step:
            break

    return OptimizationResult(parameters=params, energy=energy, history=history)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Hamiltonian-energy example from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", default="simulator", help="IonQ backend to target")
    parser.add_argument("--shots", type=int, default=100, help="Shots per energy evaluation")
    parser.add_argument("--initial-theta", type=float, default=1.2, help="Initial RY angle")
    parser.add_argument("--iterations", type=int, default=4, help="Maximum coordinate-search iterations")
    parser.add_argument("--step", type=float, default=0.4, help="Initial coordinate-search step")
    parser.add_argument("--poll-interval", type=float, default=1.0, help="Initial polling interval in seconds")
    parser.add_argument("--timeout", type=float, default=300.0, help="Polling timeout per submitted job")
    args = parser.parse_args(argv)

    client = IonQClient()

    def energy_fn(params: list[float]) -> float:
        return evaluate_energy(
            client,
            params,
            backend=args.backend,
            shots=args.shots,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )

    result = coordinate_search(
        energy_fn,
        [args.initial_theta],
        step_size=args.step,
        max_iterations=args.iterations,
    )
    print(f"final_energy={result.energy:.12g}")
    print(f"optimal_parameters={result.parameters}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
