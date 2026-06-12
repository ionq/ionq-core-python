# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for post-processing IonQ probability results."""

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

import math
from collections.abc import Mapping, Sequence


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert probabilities to integer counts using largest-remainder rounding.

    Args:
        probabilities: Mapping of integer state labels to probabilities.
        shots: Number of shots to apportion across the probability distribution.

    Returns:
        Counts whose values sum exactly to ``shots`` for normalized inputs.

    Raises:
        ValueError: If ``shots`` is negative.
    """
    if shots < 0:
        raise ValueError("shots must be non-negative")

    scaled = {state: probability * shots for state, probability in probabilities.items()}
    counts = {state: math.floor(value) for state, value in scaled.items()}
    remaining = shots - sum(counts.values())
    fractional_parts = sorted(
        scaled.items(),
        key=lambda item: (item[1] - math.floor(item[1]), item[0]),
        reverse=True,
    )

    for state, _ in fractional_parts[:remaining]:
        counts[state] += 1

    return counts


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys as zero-padded computational-basis bitstrings.

    Args:
        probabilities: Mapping of integer state labels to probabilities.
        num_qubits: Width of the output bitstrings.

    Returns:
        A new mapping with labels such as ``"00"`` and ``"11"``.

    Raises:
        ValueError: If ``num_qubits`` is negative or a state key is invalid.
    """
    _validate_num_qubits(num_qubits)
    return {
        f"{_state_index(state, num_qubits):0{num_qubits}b}": probability for state, probability in probabilities.items()
    }


def marginal(
    probabilities: Mapping[str, float],
    qubits: Sequence[int],
    num_qubits: int,
) -> dict[str, float]:
    """Marginalize a probability distribution over selected qubits.

    Qubit indices are little-endian, so qubit ``0`` is the least significant bit
    of each integer state label. Output bitstrings follow the requested
    ``qubits`` order.

    Args:
        probabilities: Mapping of integer state labels to probabilities.
        qubits: Qubit indices to keep.
        num_qubits: Number of qubits represented by the input state labels.

    Returns:
        Marginal probabilities over the requested qubits.

    Raises:
        ValueError: If ``num_qubits``, ``qubits``, or a state key is invalid.
    """
    _validate_num_qubits(num_qubits)
    _validate_qubits(qubits, num_qubits)

    marginalized: dict[str, float] = {}
    for state, probability in probabilities.items():
        state_index = _state_index(state, num_qubits)
        bitstring = "".join("1" if state_index & (1 << qubit) else "0" for qubit in qubits)
        marginalized[bitstring] = marginalized.get(bitstring, 0.0) + probability

    return marginalized


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the all-qubit Pauli-Z parity expectation value.

    Args:
        probabilities: Mapping of integer state labels to probabilities.
        num_qubits: Number of qubits represented by the input state labels.

    Returns:
        The even-minus-odd parity expectation value.

    Raises:
        ValueError: If ``num_qubits`` is negative or a state key is invalid.
    """
    _validate_num_qubits(num_qubits)
    return sum(
        (1 if _state_index(state, num_qubits).bit_count() % 2 == 0 else -1) * probability
        for state, probability in probabilities.items()
    )


def _validate_num_qubits(num_qubits: int) -> None:
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")


def _validate_qubits(qubits: Sequence[int], num_qubits: int) -> None:
    if len(set(qubits)) != len(qubits):
        raise ValueError("qubits must not contain duplicate indices")

    for qubit in qubits:
        if qubit < 0 or qubit >= num_qubits:
            raise ValueError("qubits must be in range for num_qubits")


def _state_index(state: str, num_qubits: int) -> int:
    try:
        state_index = int(state)
    except ValueError as exc:
        raise ValueError("state keys must be integer strings") from exc

    if state_index < 0:
        raise ValueError("state keys must be non-negative")

    if state_index >= 1 << num_qubits:
        raise ValueError("state keys must fit within num_qubits")

    return state_index
