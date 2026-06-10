# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Variational Hamiltonian-energy minimization on IonQ's free simulator.

Hamiltonian
    H2 molecule at equilibrium bond length (STO-3G, Jordan-Wigner, 2 qubits):
    ``0.1714·IZ + 0.1714·ZI + 0.1687·ZZ`` (Hartree). The ``II`` identity term
    (``-0.0113`` Ha) is omitted - it is a constant energy shift and the API
    ignores ``"II"`` Pauli strings. The exact ground state including that
    offset is ~ ``-1.137`` Ha.

Ansatz
    Hardware-efficient OpenQASM 3 circuit: Ry/Rz on each qubit, CNOT, Ry/Rz
    again (eight parameters), matching the Hosted Hybrid guide pattern.

Optimizer
    Hand-rolled SPSA (no scipy). Two energy evaluations per iteration; tracks
    the best energy seen across every evaluation.

Each energy evaluation builds typed ``ionq_core.models`` payloads, calls
``create_job``, ``wait_for_job``, then reads ``results["value"]`` from the
raw job JSON (the typed ``CircuitJobResult`` model omits it).
"""

from __future__ import annotations

import json
import logging
import math
import random
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from ionq_core import IonQClient, wait_for_job
from ionq_core.api.default import create_job, get_job
from ionq_core.models.ansatz import Ansatz
from ionq_core.models.hamiltonian_energy_data import HamiltonianEnergyData
from ionq_core.models.hamiltonian_energy_input import HamiltonianEnergyInput
from ionq_core.models.hamiltonian_energy_input_data import HamiltonianEnergyInputData
from ionq_core.models.hamiltonian_pauli_term import HamiltonianPauliTerm
from ionq_core.models.quantum_function_job_creation_payload import QuantumFunctionJobCreationPayload

if TYPE_CHECKING:
    from ionq_core.client import AuthenticatedClient

logger = logging.getLogger(__name__)

# H2 (STO-3G, r = 0.735 Å). Submit only non-identity Pauli terms; II is a constant offset.
H2_HAMILTONIAN: tuple[tuple[str, float], ...] = (
    ("IZ", 0.171413198),
    ("ZI", 0.171413198),
    ("ZZ", 0.168688319),
)
# Exact ground state of the full operator (including the omitted II term).
H2_EXACT_GROUND_HA = -1.1372813
H2_IDENTITY_OFFSET_HA = -0.011280524

# Ry/Rz layer, CNOT, Ry/Rz layer — scalar inputs (Qiskit qasm3 style).
H2_ANSAZ_QASM = """\
OPENQASM 3.0;
include "stdgates.inc";
input float[64] theta0;
input float[64] theta1;
input float[64] theta2;
input float[64] theta3;
input float[64] theta4;
input float[64] theta5;
input float[64] theta6;
input float[64] theta7;
qubit[2] q;
ry(theta0) q[0];
rz(theta1) q[0];
ry(theta2) q[1];
rz(theta3) q[1];
cx q[0], q[1];
ry(theta4) q[0];
rz(theta5) q[0];
ry(theta6) q[1];
rz(theta7) q[1];
"""

NUM_PARAMS = 8
SHOTS = 1000
JOB_TIMEOUT_S = 300.0
SPSA_MAXITER = 20
SPSA_LEARNING_RATE = 0.1
SPSA_PERTURBATION = 0.3


@dataclass(frozen=True)
class Problem:
    """Fixed Hamiltonian and ansatz; params vary per evaluation."""

    hamiltonian: tuple[HamiltonianPauliTerm, ...]
    ansatz: Ansatz


def build_problem() -> Problem:
    terms = tuple(HamiltonianPauliTerm(pauli_string=s, coefficient=c) for s, c in H2_HAMILTONIAN)
    return Problem(hamiltonian=terms, ansatz=Ansatz(data=H2_ANSAZ_QASM))


def initial_params(*, seed: int = 42) -> list[float]:
    rng = random.Random(seed)
    return [rng.uniform(0.0, 2.0 * math.pi) for _ in range(NUM_PARAMS)]


def _energy_from_block(block: Mapping[str, Any]) -> float | None:
    value = block.get("value")
    if value is None:
        return None
    return float(value)


def _energy_from_job(client: AuthenticatedClient, job_id: str) -> float:
    # Quantum-function jobs put energy in results.value; the typed CircuitJobResult model drops it.
    resp = get_job.sync_detailed(uuid=job_id, client=client)
    if resp.status_code.value != 200:
        raise RuntimeError(f"get_job {job_id} returned HTTP {resp.status_code.value}")
    body = json.loads(resp.content)
    for section in ("results", "output"):
        block = body.get(section)
        if isinstance(block, dict):
            energy = _energy_from_block(block)
            if energy is not None:
                return energy
    results = body.get("results")
    output = body.get("output")
    raise ValueError(f"completed job {job_id} missing results/output value; results={results!r}, output={output!r}")


def evaluate_energy(
    client: AuthenticatedClient,
    problem: Problem,
    params: Sequence[float],
) -> tuple[str, float]:
    """Submit one hamiltonian-energy job and return ``(job_id, energy)``."""
    payload = QuantumFunctionJobCreationPayload(
        backend="simulator",
        type_="quantum-function",
        name="hamiltonian-energy-vqe",
        shots=SHOTS,
        input_=HamiltonianEnergyInput(
            data=HamiltonianEnergyInputData(
                type_="hamiltonian-energy",
                data=HamiltonianEnergyData(
                    hamiltonian=list(problem.hamiltonian),
                    ansatz=problem.ansatz,
                ),
            ),
            params=list(params),
        ),
    )
    created = create_job.sync(client=client, body=payload)
    if created is None:
        raise RuntimeError("create_job returned None")
    wait_for_job(client, created.id, timeout=JOB_TIMEOUT_S)
    energy = _energy_from_job(client, created.id)
    logger.info("job=%s params=%s energy=%.6f", created.id, [round(p, 4) for p in params], energy)
    return created.id, energy


def spsa_minimize(
    objective: Callable[[list[float]], float],
    x0: list[float],
    *,
    maxiter: int = SPSA_MAXITER,
    learning_rate: float = SPSA_LEARNING_RATE,
    perturbation: float = SPSA_PERTURBATION,
    lr_decay: float = 0.602,
    pert_decay: float = 0.101,
    stability: float = 1.0,
    seed: int = 0,
) -> tuple[list[float], float]:
    """Simultaneous perturbation stochastic approximation (gradient-free).

    Uses two objective evaluations per iteration (θ±δ). The returned optimum
    is the lowest energy seen across every evaluation, not just the final θ.
    """
    rng = random.Random(seed)
    params = list(x0)
    best_params = params[:]
    best_val = objective(params)
    print(f"iter   0/{maxiter} energy = {best_val:+.6f}  best = {best_val:+.6f}")

    for k in range(1, maxiter + 1):
        ak = learning_rate / (k + stability) ** lr_decay
        ck = perturbation / k**pert_decay
        delta = [rng.choice([-1.0, 1.0]) for _ in params]
        x_plus = [xi + ck * di for xi, di in zip(params, delta, strict=True)]
        x_minus = [xi - ck * di for xi, di in zip(params, delta, strict=True)]
        y_plus = objective(x_plus)
        y_minus = objective(x_minus)
        if y_plus < best_val:
            best_val = y_plus
            best_params = x_plus[:]
        if y_minus < best_val:
            best_val = y_minus
            best_params = x_minus[:]
        gradient = [(y_plus - y_minus) / (2.0 * ck) * di for di in delta]
        params = [xi - ak * gi for xi, gi in zip(params, gradient, strict=True)]
        print(f"iter {k:>3}/{maxiter} E+ = {y_plus:+.6f} E- = {y_minus:+.6f} best = {best_val:+.6f}")

    return best_params, best_val


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = IonQClient(additional_user_agent="ionq-core-example/hamiltonian-energy-vqe")
    problem = build_problem()
    params0 = initial_params()

    print("H2 VQE on simulator (hamiltonian-energy quantum function)")
    print(f"  Hamiltonian: {len(problem.hamiltonian)} Pauli terms (STO-3G, r = 0.735 Å)")
    print(f"  Exact ground energy (incl. omitted II term): {H2_EXACT_GROUND_HA:+.4f} Ha")
    print(f"  Ansatz: Ry/Rz + CNOT + Ry/Rz ({NUM_PARAMS} parameters)")
    print(f"  Optimizer: SPSA, maxiter={SPSA_MAXITER}, shots={SHOTS}")
    print("  Expect best energy roughly -0.15 to -0.25 Ha with this shallow demo ansatz.")
    print(f"  Initial params: {[round(p, 4) for p in params0]}")
    print()

    eval_count = 0

    def energy_fn(p: list[float]) -> float:
        nonlocal eval_count
        eval_count += 1
        job_id, energy = evaluate_energy(client, problem, p)
        print(f"  [eval {eval_count:>2}] job={job_id} energy={energy:+.6f} params={[round(x, 4) for x in p]}")
        return energy

    optimal_params, optimal_energy = spsa_minimize(energy_fn, params0)
    shifted_energy = optimal_energy + H2_IDENTITY_OFFSET_HA
    print()
    print(f"Optimization complete ({eval_count} energy evaluations)")
    print(f"Best energy (submitted Hamiltonian): {optimal_energy:+.8f} Ha")
    print(f"Shifted by II offset ({H2_IDENTITY_OFFSET_HA:+.6f} Ha): {shifted_energy:+.8f} Ha")
    print(f"Exact ground state reference: {H2_EXACT_GROUND_HA:+.8f} Ha")
    print(f"Best params: {[round(p, 6) for p in optimal_params]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
