# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Optimize a two-qubit Hamiltonian Energy quantum function on the simulator.

Hamiltonian:
    H = -1.0 * ZI - 1.0 * IZ + 0.5 * ZZ

Ansatz:
    A compact two-qubit QIS-style ansatz serialized into `Ansatz.data`, with
    two rotation parameters followed by a CNOT entangler.

Optimizer:
    A dependency-free coordinate search. Each iteration evaluates the current
    parameter vector and one positive/negative step along every coordinate,
    then halves the step size before the next iteration.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import cast

from ionq_core import AuthenticatedClient, IonQClient, wait_for_job
from ionq_core.api.default import create_job
from ionq_core.models import (
    Ansatz,
    HamiltonianEnergyData,
    HamiltonianEnergyInput,
    HamiltonianEnergyInputData,
    HamiltonianPauliTerm,
    JobCreationResponse,
    QuantumFunctionJobCreationPayload,
)

INITIAL_PARAMS = [0.1, 0.4]
ITERATIONS = 4
SHOTS = 100

# `Ansatz.data` is intentionally a string in the public API. This payload keeps
# the example self-contained and mirrors IonQ's JSON circuit shape.
ANSATZ_DATA = json.dumps(
    {
        "qubits": 2,
        "gateset": "qis",
        "circuit": [
            {"gate": "ry", "target": 0, "rotation": "theta_0"},
            {"gate": "ry", "target": 1, "rotation": "theta_1"},
            {"gate": "cnot", "control": 0, "target": 1},
        ],
        "parameters": ["theta_0", "theta_1"],
    },
    separators=(",", ":"),
)


def build_hamiltonian_energy_payload(params: list[float]) -> QuantumFunctionJobCreationPayload:
    """Build a typed Hamiltonian Energy job payload for one parameter vector."""
    return QuantumFunctionJobCreationPayload(
        backend="simulator",
        type_="quantum-function",
        shots=SHOTS,
        name="Hamiltonian energy coordinate search",
        input_=HamiltonianEnergyInput(
            data=HamiltonianEnergyInputData(
                type_="hamiltonian-energy",
                data=HamiltonianEnergyData(
                    hamiltonian=[
                        HamiltonianPauliTerm(pauli_string="ZI", coefficient=-1.0),
                        HamiltonianPauliTerm(pauli_string="IZ", coefficient=-1.0),
                        HamiltonianPauliTerm(pauli_string="ZZ", coefficient=0.5),
                    ],
                    ansatz=Ansatz(data=ANSATZ_DATA),
                ),
            ),
            params=params,
        ),
    )


def evaluate_energy(client: AuthenticatedClient, params: list[float]) -> float:
    """Submit one Hamiltonian Energy job and return its completed energy."""
    submitted = create_job.sync(client=client, body=build_hamiltonian_energy_payload(params))
    if not isinstance(submitted, JobCreationResponse):
        msg = f"Expected JobCreationResponse, received {type(submitted).__name__}"
        raise RuntimeError(msg)

    completed = wait_for_job(client, submitted.id)
    return extract_energy(completed.output.to_dict())


def extract_energy(output: Mapping[str, object]) -> float:
    """Extract an energy value from common quantum-function response shapes."""
    direct = _first_numeric(output, ("energy", "value", "expectation_value", "minimum_value"))
    if direct is not None:
        return direct

    for nested_key in ("result", "results", "solution", "output"):
        nested = output.get(nested_key)
        if isinstance(nested, Mapping):
            if not all(isinstance(key, str) for key in nested):
                continue
            nested_value = _first_numeric(
                cast(Mapping[str, object], nested),
                ("energy", "value", "expectation_value", "minimum_value"),
            )
            if nested_value is not None:
                return nested_value

    msg = f"Could not find an energy value in job output keys: {sorted(output)}"
    raise RuntimeError(msg)


def coordinate_search(
    evaluate: Callable[[list[float]], float],
    initial_params: list[float],
    *,
    iterations: int = ITERATIONS,
    step: float = 0.4,
) -> tuple[list[float], float]:
    """Minimize an energy callback with a small coordinate-search loop."""
    params = list(initial_params)
    best_energy = evaluate(params)

    for iteration in range(1, iterations + 1):
        for index in range(len(params)):
            for direction in (1.0, -1.0):
                candidate = list(params)
                candidate[index] += direction * step
                candidate_energy = evaluate(candidate)
                if candidate_energy < best_energy:
                    params = candidate
                    best_energy = candidate_energy
        print(f"iteration={iteration} energy={best_energy:.8f} params={params}")
        step *= 0.5

    return params, best_energy


def _first_numeric(values: Mapping[str, object], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        value = values.get(key)
        if isinstance(value, int | float):
            return float(value)
    return None


def main() -> None:
    """Run the optimization loop."""
    client = IonQClient()
    best_params, best_energy = coordinate_search(lambda params: evaluate_energy(client, params), INITIAL_PARAMS)
    print(f"final_energy={best_energy:.8f}")
    print(f"final_params={best_params}")


if __name__ == "__main__":
    main()
