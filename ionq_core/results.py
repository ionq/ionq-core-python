# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for post-processing IonQ probability results.

IonQ result payloads encode measured basis states as integer strings. These
helpers treat qubit 0 as the least significant bit of that integer key.
"""

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

import math
from collections.abc import Iterable, Mapping


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert a probability distribution to integer shot counts.

    Counts are rounded with the largest-remainder method and always sum exactly
    to ``shots``. Input probabilities must be finite, non-negative, and sum to 1
    within floating-point tolerance.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        shots: Number of shots to distribute.

    Returns:
        A mapping with the same keys and integer counts summing to ``shots``.
    """
    if shots < 0:
        raise ValueError("shots must be non-negative")

    scaled: list[tuple[str, int, float, int]] = []
    total_probability = 0.0
    for order, (key, probability) in enumerate(probabilities.items()):
        probability = _validate_probability(probability, f"probabilities[{key!r}]")
        total_probability += probability
        expected_count = probability * shots
        floor_count = math.floor(expected_count)
        scaled.append((key, floor_count, expected_count - floor_count, order))

    if not scaled:
        if shots == 0:
            return {}
        raise ValueError("probabilities must not be empty when shots is positive")

    if not math.isclose(total_probability, 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("probabilities must sum to 1")

    counts = {key: floor_count for key, floor_count, _, _ in scaled}
    remaining = shots - sum(counts.values())
    if remaining:
        for key, _, _, _ in sorted(scaled, key=lambda item: (-item[2], item[3]))[:remaining]:
            counts[key] += 1
    return counts


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer-encoded state keys to zero-padded bitstrings.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        num_qubits: Width of the measured register.

    Returns:
        A mapping from bitstring labels to probabilities.
    """
    _validate_num_qubits(num_qubits)
    return {
        format(_parse_state_key(key, num_qubits), f"0{num_qubits}b"): _validate_probability(
            probability, f"probabilities[{key!r}]"
        )
        for key, probability in probabilities.items()
    }


def marginal(probabilities: Mapping[str, float], qubits: Iterable[int], num_qubits: int) -> dict[str, float]:
    """Return the probability marginal over a subset of qubits.

    Qubit indices are interpreted little-endian: qubit 0 is the least
    significant bit of the integer state key. The returned marginal key uses the
    order supplied in ``qubits``; the first selected qubit becomes bit 0 in the
    reduced integer key.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        qubits: Qubits to keep in the returned marginal.
        num_qubits: Width of the measured register.

    Returns:
        A probability mapping over the selected qubits.
    """
    selected_qubits = _normalize_qubits(qubits, num_qubits)
    reduced: dict[str, float] = {}
    for key, probability in probabilities.items():
        state = _parse_state_key(key, num_qubits)
        probability = _validate_probability(probability, f"probabilities[{key!r}]")
        reduced_key = str(_project_state(state, selected_qubits))
        reduced[reduced_key] = reduced.get(reduced_key, 0.0) + probability
    return reduced


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the parity expectation value for ``Z`` on every measured qubit.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        num_qubits: Width of the measured register.

    Returns:
        The expectation value ``sum(p(x) * (-1) ** popcount(x))``.
    """
    _validate_num_qubits(num_qubits)
    expectation = 0.0
    for key, probability in probabilities.items():
        state = _parse_state_key(key, num_qubits)
        probability = _validate_probability(probability, f"probabilities[{key!r}]")
        expectation += probability if state.bit_count() % 2 == 0 else -probability
    return expectation


def _normalize_qubits(qubits: Iterable[int], num_qubits: int) -> tuple[int, ...]:
    _validate_num_qubits(num_qubits)
    selected_qubits = tuple(qubits)
    seen: set[int] = set()
    for qubit in selected_qubits:
        if qubit < 0 or qubit >= num_qubits:
            raise ValueError(f"qubit index {qubit} is outside the {num_qubits}-qubit register")
        if qubit in seen:
            raise ValueError(f"qubit index {qubit} is repeated")
        seen.add(qubit)
    return selected_qubits


def _parse_state_key(key: str, num_qubits: int) -> int:
    try:
        state = int(key)
    except ValueError as exc:
        raise ValueError(f"state key {key!r} is not an integer") from exc

    if state < 0 or state >= 1 << num_qubits:
        raise ValueError(f"state key {key!r} is outside the {num_qubits}-qubit register")
    return state


def _project_state(state: int, qubits: tuple[int, ...]) -> int:
    reduced_state = 0
    for output_bit, qubit in enumerate(qubits):
        reduced_state |= ((state >> qubit) & 1) << output_bit
    return reduced_state


def _validate_num_qubits(num_qubits: int) -> None:
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")


def _validate_probability(probability: float, label: str) -> float:
    if not math.isfinite(probability):
        raise ValueError(f"{label} must be finite")
    if probability < 0:
        raise ValueError(f"{label} must be non-negative")
    return probability
