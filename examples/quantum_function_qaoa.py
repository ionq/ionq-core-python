# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""
Quantum Function QAOA Example
=============================

This example demonstrates how to use IonQ's Hosted Hybrid Service (Quantum Functions)
to solve a Max Cut problem using the Quantum Approximate Optimization Algorithm (QAOA).

- Problem: Max Cut on a 3-vertex graph with edges (0, 1) and (1, 2)
- Graph (3 nodes, 2 edges): 0 -- 1 -- 2
- Objective Function: max \sum_{i, j \in E} (x_i x_j - x_i - x_j)
- Hamiltonian: H_c = 0.5 * (Z_0 Z_1 + Z_1 Z_2) (Energy minimization ignoring constant terms)
- Ansatz: 1 layer QAOA with Pauli X mixer
- Optimizer: SLSQP with bounds via scipy.optimize
"""

import math
import os
import time

import scipy.optimize  # type: ignore

from ionq_core import IonQClient, wait_for_job
from ionq_core.api.default import create_job
from ionq_core.models import (
    Ansatz,
    HamiltonianEnergyData,
    HamiltonianEnergyInput,
    HamiltonianEnergyInputData,
    HamiltonianPauliTerm,
    QuantumFunctionJobCreationPayload,
)

# 1. Initialize the IonQ client
client = IonQClient()


# 2. Define the Max Cut problem Hamiltonian (Hc)
hamiltonian_terms = [
    HamiltonianPauliTerm(pauli_string="Z0 Z1", coefficient=0.5),
    HamiltonianPauliTerm(pauli_string="Z1 Z2", coefficient=0.5),
]


# 3. Define the Ansatz with QASM 3.0 parameters
# We define `p0` (gamma) and `p1` (2*beta) as inputs.
qasm_str = """OPENQASM 3.0;
include "stdgates.inc";

input float[64] p0;
input float[64] p1;

qubit[3] q;

h q[0];
h q[1];
h q[2];

rzz(p0) q[0], q[1];
rzz(p0) q[1], q[2];

rx(p1) q[0];
rx(p1) q[1];
rx(p1) q[2];
"""

ansatz = Ansatz(data=qasm_str)
energy_data = HamiltonianEnergyData(hamiltonian=hamiltonian_terms, ansatz=ansatz)
input_data = HamiltonianEnergyInputData(type_="hamiltonian-energy", data=energy_data)


# 4. Define the objective function (Energy evaluation)
def evaluate_energy(params: list[float]) -> float:
    """
    Evaluates the energy of the QAOA ansatz for the given parameters.

    Args:
        params: A list of two floats [gamma, beta] for QAOA p=1.

    Returns:
        The expected energy value.
    """
    gamma, beta = params

    # We pass the parameters natively through the Quantum Function's `params` field.
    energy_input = HamiltonianEnergyInput(
        data=input_data,
        params=[gamma, 2.0 * beta],
    )

    payload = QuantumFunctionJobCreationPayload(
        backend="simulator",  # Using the free cloud simulator
        type_="quantum-function",
        input_=energy_input,
    )

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            # Submit the job to the IonQ API
            job = create_job.sync(client=client, body=payload)
            if job is None or not hasattr(job, "id"):
                raise RuntimeError(f"Job creation failed or returned malformed response: {job}")

            # Wait for completion and parse result
            # `wait_for_job` will raise exceptions on timeouts or if the job transitions to 'failed'
            completed = wait_for_job(client, job.id)
            if completed.status == "canceled":
                raise RuntimeError("Job was unexpectedly canceled by the backend.")

            # For Quantum Function jobs, the algorithmic result is returned in the flexible `output` block
            energy = float(completed.output["energy"])

            print(f"Iter: gamma={gamma:.4f}, beta={beta:.4f} | Energy: {energy:.4f}")
            return energy

        except Exception as e:
            print(f"  [Warning] Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("  [Error] Max retries reached. Aborting optimization.")
                raise

            time.sleep(2)

    raise RuntimeError("Unreachable")


if __name__ == "__main__":
    # Ensure API Key is available before starting
    if not os.getenv("IONQ_API_KEY"):
        raise RuntimeError("Please set the IONQ_API_KEY environment variable.")

    # Initial guess for [gamma, beta]
    initial_params = [0.5, 0.5]

    # Use a classical optimizer to minimize the energy callback
    # Note: OpenQASM 2.0 rx/rz gates expect angles in radians.
    bounds = [(0.0, 2 * math.pi), (0.0, math.pi)]

    print(f"Starting optimization with initial parameters: {initial_params}, expecting minimum energy -2")

    result = scipy.optimize.minimize(
        evaluate_energy, initial_params, method="SLSQP", bounds=bounds, options={"maxiter": 20}
    )

    print(f"Optimal Parameters (gamma, beta): {result.x}")
    print(f"Minimum Energy Found: {result.fun}")
