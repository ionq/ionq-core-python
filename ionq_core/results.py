# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for post-processing IonQ probability results.

IonQ probability endpoints expose mappings whose keys are integer-encoded
measurement states and whose values are probabilities. The helpers here keep
that wire-level shape, but make common SDK tasks easier: deterministic shot
rounding, bitstring labels, marginals, and all-Z parity expectation values.

Bit-ordering convention:
    Integer state keys are interpreted as computational-basis integers. Qubit 0
    is the least-significant bit, so the two-qubit Bell-state probabilities
    ``{"0": 0.5, "3": 0.5}`` relabel to ``{"00": 0.5, "11": 0.5}``.
"""

from collections.abc import Iterable, Mapping
from math import floor

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert probabilities to integer shot counts using largest-remainder rounding.

    The returned counts always sum exactly to ``shots``. Ties are broken by the
    integer value of the result key, keeping output deterministic for callers and
    tests.

    Args:
        probabilities: IonQ probability mapping, keyed by integer state strings.
        shots: Total number of requested shots. Must be non-negative.

    Returns:
        A mapping with the same keys and integer counts summing to ``shots``.
    """
    if shots < 0:
        raise ValueError("shots must be non-negative")

    floors: dict[str, int] = {}
    remainders: list[tuple[float, int, str]] = []
    for key, probability in probabilities.items():
        expected = probability * shots
        count = floor(expected)
        floors[key] = count
        remainders.append((expected - count, _state_int(key), key))

    missing = shots - sum(floors.values())
    for _, _, key in sorted(remainders, key=lambda item: (-item[0], item[1], item[2]))[:missing]:
        floors[key] += 1

    return floors


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys to zero-padded computational-basis bitstrings.

    Args:
        probabilities: IonQ probability mapping, keyed by integer state strings.
        num_qubits: Width of the output bitstrings.

    Returns:
        Probabilities keyed by zero-padded bitstrings of length ``num_qubits``.
    """
    _validate_num_qubits(num_qubits)
    bitstring_probabilities: dict[str, float] = {}
    for key, probability in probabilities.items():
        bitstring = _bitstring(_state_int(key), num_qubits)
        bitstring_probabilities[bitstring] = bitstring_probabilities.get(bitstring, 0.0) + probability
    return bitstring_probabilities


def marginal(probabilities: Mapping[str, float], qubits: Iterable[int], num_qubits: int) -> dict[str, float]:
    """Marginalize probabilities onto the requested qubits.

    Qubit indices follow the integer-key convention: qubit 0 is the
    least-significant bit. The output bitstring follows the order in ``qubits``.

    Args:
        probabilities: IonQ probability mapping, keyed by integer state strings.
        qubits: Qubit indices to keep, in output order.
        num_qubits: Width of the full result register.

    Returns:
        Marginal probabilities keyed by selected-qubit bitstrings.
    """
    _validate_num_qubits(num_qubits)
    selected = tuple(qubits)
    for qubit in selected:
        if qubit < 0 or qubit >= num_qubits:
            raise ValueError("qubits must be within the result register")

    result: dict[str, float] = {}
    for key, probability in probabilities.items():
        state = _state_int(key)
        label = "".join(str((state >> qubit) & 1) for qubit in selected)
        result[label] = result.get(label, 0.0) + probability
    return result


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the all-Z parity expectation value for a probability mapping.

    The value is ``sum(probability * (-1) ** popcount(state))`` over the
    provided result states.

    Args:
        probabilities: IonQ probability mapping, keyed by integer state strings.
        num_qubits: Width of the result register.

    Returns:
        The all-Z expectation value.
    """
    _validate_num_qubits(num_qubits)
    return sum(
        probability * (-1 if _state_int(key).bit_count() % 2 else 1) for key, probability in probabilities.items()
    )


def _validate_num_qubits(num_qubits: int) -> None:
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")


def _state_int(key: str) -> int:
    state = int(key)
    if state < 0:
        raise ValueError("state keys must be non-negative integers")
    return state


def _bitstring(state: int, num_qubits: int) -> str:
    return f"{state:0{num_qubits}b}"
