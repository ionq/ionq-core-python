# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for IonQ probability mappings — no NumPy, no surprises.

IonQ result endpoints return state-key → probability dicts where
qubit 0 is the least-significant bit of the integer key (e.g. a
two-qubit Bell state appears as ``{"0": 0.5, "3": 0.5}``).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

__all__ = [
    "expectation_z",
    "marginal",
    "probabilities_to_counts",
    "relabel_to_bitstrings",
]


def _check(probabilities: Mapping[str, float]) -> None:
    """Validate that all probabilities are finite and non-negative."""
    for k, v in probabilities.items():
        if not math.isfinite(v) or v < 0:
            raise ValueError(f"Probability for state '{k}' must be finite and non-negative, got {v}.")


def probabilities_to_counts(
    probabilities: Mapping[str, float],
    shots: int,
    *,
    drop_zeros: bool = True,
) -> dict[str, int]:
    """Convert a probability mapping to integer counts.

    Uses largest-remainder rounding so the result sums exactly to ``shots``.

    Args:
        probabilities: Mapping from integer state keys to probabilities.
        shots: Total number of shots. Must be non-negative.
        drop_zeros: If True (default), omit states with zero counts.

    Returns:
        Mapping from state keys to integer counts, summing to ``shots``.

    Raises:
        ValueError: If ``shots`` is negative or any probability is non-finite.

    Example::

        probabilities_to_counts({"0": 0.5, "3": 0.5}, 100)
        # → {'0': 50, '3': 50}
    """
    if shots < 0:
        raise ValueError(f"shots must be non-negative, got {shots}.")
    if not probabilities or shots == 0:
        return {}
    _check(probabilities)

    floors = {}
    remainders = {}
    for k, v in probabilities.items():
        exact = v * shots
        f = math.floor(exact)
        floors[k] = f
        remainders[k] = exact - f

    remaining = shots - sum(floors.values())
    if remaining:
        for k in sorted(remainders, key=remainders.get, reverse=True)[:remaining]:
            floors[k] += 1

    if drop_zeros:
        return {k: v for k, v in floors.items() if v}
    return floors


def relabel_to_bitstrings(
    probabilities: Mapping[str, float],
    num_qubits: int,
    *,
    little_endian: bool = False,
) -> dict[str, float]:
    """Relabel integer state keys to zero-padded bitstrings.

    Args:
        probabilities: Mapping from integer state keys to probabilities.
        num_qubits: Number of qubits to pad to.
        little_endian: If True, qubit 0 appears on the left (reversed).

    Returns:
        Mapping from bitstring keys to the same probabilities.

    Raises:
        ValueError: If any state key exceeds the range of ``num_qubits``.

    Example::

        relabel_to_bitstrings({"0": 0.5, "3": 0.5}, 2)
        # → {'00': 0.5, '11': 0.5}

        relabel_to_bitstrings({"0": 0.5, "3": 0.5}, 2, little_endian=True)
        # → {'00': 0.5, '11': 0.5}
    """
    max_state = (1 << num_qubits) - 1
    result = {}
    for key, prob in probabilities.items():
        s = int(key)
        if not 0 <= s <= max_state:
            raise ValueError(f"State {s} out of bounds for {num_qubits} qubits (max {max_state}).")
        bs = f"{s:0{num_qubits}b}"
        result[bs[::-1] if little_endian else bs] = prob
    return result


def marginal(
    probabilities: Mapping[str, float],
    qubits: Sequence[int],
    num_qubits: int,
) -> dict[str, float]:
    """Marginal probability distribution over a subset of qubits.

    ``qubits[0]`` is the most significant position in the output key.

    Args:
        probabilities: Mapping from integer state keys to probabilities.
        qubits: Qubit indices to keep (qubit 0 is the LSB).
        num_qubits: Total qubits in the input distribution.

    Returns:
        Mapping from output integer keys to marginal probabilities.

    Raises:
        ValueError: If ``qubits`` is empty, has duplicates, or has out-of-range indices.

    Example::

        marginal({"0": 0.5, "3": 0.5}, [0], 2)
        # → {'0': 0.5, '1': 0.5}
    """
    if not qubits:
        raise ValueError("qubits must not be empty.")
    if len(set(qubits)) != len(qubits):
        raise ValueError("qubits must not contain duplicates.")
    for q in qubits:
        if q < 0 or q >= num_qubits:
            raise ValueError(f"Qubit index {q} out of bounds for {num_qubits} qubits.")

    n = len(qubits)
    result: dict[str, float] = {}
    for key, prob in probabilities.items():
        s = int(key)
        out = 0
        for i, q in enumerate(qubits):
            out |= ((s >> q) & 1) << (n - 1 - i)
        sk = str(out)
        result[sk] = result.get(sk, 0.0) + prob
    return result


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    r"""⟨Z⊗⋯⊗Z⟩ — parity expectation value over all measured qubits.

    States with even popcount contribute +1.p; odd popcount -1.p.

    Args:
        probabilities: Mapping from integer state keys to probabilities.
        num_qubits: Total number of qubits.

    Returns:
        The Z-parity expectation value in [-1, +1].

    Raises:
        ValueError: If any state key exceeds the range of ``num_qubits``.

    Example::

        expectation_z({"0": 0.5, "3": 0.5}, 2)
        # → 1.0
    """
    max_state = (1 << num_qubits) - 1
    total = 0.0
    for key, prob in probabilities.items():
        s = int(key)
        if not 0 <= s <= max_state:
            raise ValueError(f"State {s} out of bounds for {num_qubits} qubits (max {max_state}).")
        total += prob if s.bit_count() % 2 == 0 else -prob
    return total
