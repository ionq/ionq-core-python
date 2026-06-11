# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for post-processing IonQ probability results.

IonQ probability endpoints return mappings from integer-encoded computational
basis states to probabilities. These helpers treat qubit 0 as the least
significant bit, so state ``"1"`` on a two-qubit result is bitstring ``"01"``
when displayed in conventional most-significant-bit-first order.
"""

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

import math
from collections.abc import Iterable, Mapping


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert probabilities to integer counts that sum exactly to ``shots``.

    Counts are produced with largest-remainder rounding. Ties are broken by the
    integer state key, making the result deterministic.

    Args:
        probabilities: Mapping of integer-encoded state keys to probabilities.
        shots: Total number of shots to distribute.

    Returns:
        A count mapping with the same keys as ``probabilities``.

    Raises:
        ValueError: If ``shots`` is negative or the probabilities are not
            compatible with exact largest-remainder rounding to ``shots``.
    """
    if shots < 0:
        msg = "shots must be non-negative"
        raise ValueError(msg)

    quotas = {state: probability * shots for state, probability in probabilities.items()}
    counts = {state: math.floor(quota) for state, quota in quotas.items()}
    remaining = shots - sum(counts.values())

    if remaining < 0 or remaining > len(counts):
        msg = "probabilities must sum close enough to 1 to allocate exactly shots counts"
        raise ValueError(msg)
    if remaining == 0:
        return counts

    ranked_states = sorted(quotas, key=lambda state: (-(quotas[state] - counts[state]), _state_index(state)))
    for state in ranked_states[:remaining]:
        counts[state] += 1
    return counts


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys as zero-padded bitstrings.

    Bitstrings are returned most-significant-bit first for readability. Qubit 0
    is the least significant bit, so state ``"1"`` becomes ``"01"`` for
    ``num_qubits=2``.

    Args:
        probabilities: Mapping of integer-encoded state keys to probabilities.
        num_qubits: Number of measured qubits.

    Returns:
        A probability mapping keyed by zero-padded bitstrings.
    """
    _validate_num_qubits(num_qubits)
    return {
        format(_parse_state_key(state, num_qubits), f"0{num_qubits}b"): probability
        for state, probability in probabilities.items()
    }


def marginal(probabilities: Mapping[str, float], qubits: Iterable[int], num_qubits: int) -> dict[str, float]:
    """Compute a marginal probability distribution over selected qubits.

    The output bitstring follows the order of ``qubits``. For example, with
    ``qubits=[0, 2]``, the first output bit is qubit 0 and the second output bit
    is qubit 2. Qubit 0 is the least significant bit of each integer state key.

    Args:
        probabilities: Mapping of integer-encoded state keys to probabilities.
        qubits: Qubit indices to keep.
        num_qubits: Number of measured qubits.

    Returns:
        A probability mapping over the selected qubits.
    """
    selected = _validate_qubits(qubits, num_qubits)
    marginals: dict[str, float] = {}
    for state_key, probability in probabilities.items():
        state = _parse_state_key(state_key, num_qubits)
        projected = "".join("1" if state & (1 << qubit) else "0" for qubit in selected)
        marginals[projected] = marginals.get(projected, 0.0) + probability
    return marginals


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the full-register ``Z tensor ... tensor Z`` expectation value.

    This is ``sum(p(x) * (-1) ** popcount(x))`` over all integer-encoded states.
    Qubit 0 is the least significant bit.

    Args:
        probabilities: Mapping of integer-encoded state keys to probabilities.
        num_qubits: Number of measured qubits.

    Returns:
        The parity expectation value.
    """
    _validate_num_qubits(num_qubits)
    total = 0.0
    for state_key, probability in probabilities.items():
        state = _parse_state_key(state_key, num_qubits)
        sign = -1.0 if state.bit_count() % 2 else 1.0
        total += sign * probability
    return total


def _state_index(state: str) -> int:
    return int(state)


def _parse_state_key(state: str, num_qubits: int) -> int:
    parsed = _state_index(state)
    if parsed < 0 or parsed >= 1 << num_qubits:
        msg = f"state key {state!r} does not fit in {num_qubits} qubits"
        raise ValueError(msg)
    return parsed


def _validate_num_qubits(num_qubits: int) -> None:
    if num_qubits < 0:
        msg = "num_qubits must be non-negative"
        raise ValueError(msg)


def _validate_qubits(qubits: Iterable[int], num_qubits: int) -> tuple[int, ...]:
    _validate_num_qubits(num_qubits)
    selected = tuple(qubits)
    if len(set(selected)) != len(selected):
        msg = "qubits must not contain duplicates"
        raise ValueError(msg)
    for qubit in selected:
        if qubit < 0 or qubit >= num_qubits:
            msg = f"qubit {qubit} is outside the range [0, {num_qubits})"
            raise ValueError(msg)
    return selected
