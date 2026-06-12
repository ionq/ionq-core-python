# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python results post-processing helpers.

This module provides helpers over the register-keyed probability mapping
returned by IonQ's results endpoints.


"""

__all__ = [
    "expectation_z",
    "marginal",
    "probabilities_to_counts",
    "relabel_to_bitstrings",
]

import math
from collections import defaultdict
from collections.abc import Mapping, Sequence



def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert a probability mapping to integer counts.

    Uses the largest-remainder method so that counts sum exactly to `shots`.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        shots: Total number of counts.

    Returns:
        Mapping from the same keys to integer counts.
    """
    if shots < 0:
        raise ValueError("Number of shots must be non-negative.")
    result = {}
    remainders = []
    remaining_shots = shots
    for state, probability in probabilities.items():
        result[state] = math.floor(probability * shots)
        remainders.append((probability * shots - result[state], state))
        remaining_shots -= result[state]
    
    remainders.sort(key=lambda x: (x[0], int(x[1])), reverse=True)
    for _remainder, state in remainders[:remaining_shots]:
        result[state] += 1
    return result
    


def relabel_to_bitstrings(
    probabilities: Mapping[str, float], num_qubits: int, little_endian: bool = False
) -> dict[str, float]:
    """Convert integer state keys to zero-padded bitstrings. Big-endian is the default bitstring ordering.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        num_qubits: Number of qubits used to pad the bitstring.
        little_endian: Whether to translate the bitstrings to little-endian (for qiskit-style libraries).

    Returns:
        Mapping from bitstrings to probabilities.
    """
    if num_qubits <= 0:
        raise ValueError("Number of qubits must be positive.")
    if _max_qubits(probabilities) >= (1 << num_qubits):
        raise ValueError(f"State {_max_qubits(probabilities)} is out of range for {num_qubits} qubits.")
    result = {}
    for state, probability in probabilities.items():
        bitstring = format(int(state), f'0{num_qubits}b')
        if little_endian:
            bitstring = bitstring[::-1]
        result[bitstring] = probability
    return result


def marginal(
    probabilities: Mapping[str, float], qubits: Sequence[int], num_qubits: int
) -> dict[str, float]:
    """Compute the marginal probabilities over a subset of qubits.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        qubits: A list of qubit indices to keep.
        num_qubits: Total number of qubits in the original state.

    Returns:
        Mapping from integer state keys (as strings) to marginal probabilities.
    """
    if min(qubits) < 0:
        raise ValueError("Qubit indices must be non-negative.")
    if num_qubits < 0:
        raise ValueError("Number of qubits must be positive.")
    if _max_qubits(probabilities) >= (1 << num_qubits):
        raise ValueError(f"State {_max_qubits(probabilities)} is out of range for {num_qubits} qubits.")
    if max(qubits) >= num_qubits:
        raise ValueError("Qubit indices must be less than the number of qubits.")
    if len(set(qubits)) != len(qubits):
        raise ValueError("Qubits must be non-duplicated")
    result = defaultdict(float)
    for state_string, probability in probabilities.items():
        state = int(state_string)
        marginalized_state = 0
        for qubit in qubits[::-1]:
            marginalized_state = (marginalized_state << 1) + ((state >> qubit) & 1)
        result[str(marginalized_state)] += probability
    
    return dict(result)


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Calculate the expectation value of the Z-basis observable.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        num_qubits: Total number of qubits.

    Returns:
        Expectation value in the range [-1.0, 1.0].
    """
    if num_qubits < 0:
        raise ValueError("Number of qubits must be positive.")
    if _max_qubits(probabilities) >= (1 << num_qubits):
        raise ValueError(f"State {_max_qubits(probabilities)} is out of range for {num_qubits} qubits.")
    result = 0
    for state, probability in probabilities.items():
        result += (1 - 2 * (int(state).bit_count() & 1)) * probability
    return result

def _max_qubits(probabilities: Mapping[str, float]) -> int:
    """Validate that `num_qubits` is mathematically sufficient to represent all states."""
    if not probabilities:
        return -1
    return max(int(state) for state in probabilities)
    
    