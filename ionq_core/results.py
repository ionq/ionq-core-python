# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python results post-processing helpers.

This module provides helpers over the register-keyed probability mapping
returned by IonQ's results endpoints.

Qubit ordering:
    IonQ probability results map integer state keys (as strings) to
    probabilities.  Throughout this module, qubit i corresponds to
    bit 2^i in the integer key -- i.e. qubit 0 is the least significant bit (LSB).

    For example, given a 3-qubit circuit the integer key ``4``
    (binary ``100``) encodes qubit 0 = 0, qubit 1 = 0, qubit 2 = 1.

Example:
    ```python
    from ionq_core import probabilities_to_counts, relabel_to_bitstrings, marginal, expectation_z

    counts = probabilities_to_counts({"0": 0.4, "3": 0.6}, 100)  # translate probability results into counts
    bitstrings = relabel_to_bitstrings({"0": 0.4, "3": 0.6}, 2)  # relabel to bitstrings
    marginal_probabilities = marginal({"0": 0.4, "3": 0.6}, [0], 2)  # compute the marginal probabilities over qubit 0
    expectation = expectation_z({"0": 0.4, "3": 0.6}, 2)  # compute the expectation value of the Z-basis observable
    ```
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

    Raises:
        ValueError: If ``shots`` is negative.

    Examples:
        ```python
        >>> probabilities_to_counts({"0": 0.4, "3": 0.6}, 100)   # counts with 100 shots
        {'0': 40, '3': 60}
        ```
    """
    if shots < 0:
        raise ValueError("Number of shots must be non-negative")
    result = {}
    remainders = []
    remaining_shots = shots
    for state, probability in probabilities.items():
        result[state] = math.floor(probability * shots)
        remainders.append((probability * shots - result[state], state))
        remaining_shots -= result[state]

    remainders.sort(key=lambda x: (-x[0], int(x[1])))
    for _remainder, state in remainders[:remaining_shots]:
        result[state] += 1
    return result


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Convert integer state keys to zero-padded bitstrings.

    The most-significant bit is on the left, producing bitstrings in
    ``q(n-1) ... q1 q0`` order (qubit 0 rightmost).

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        num_qubits: Number of qubits used to pad the bitstring.

    Returns:
        Mapping from bitstrings to probabilities.

    Raises:
        ValueError: If ``num_qubits`` is not positive, or a state key does not
            fit in ``num_qubits`` qubits.

    Examples:
        ```python
        >>> relabel_to_bitstrings({"0": 0.25, "1":0.25, "2":0.25, "3":0.25}, 2)
        {'00': 0.25, '01': 0.25, '10': 0.25, '11': 0.25}
        >>> relabel_to_bitstrings({"0": 0.25, "1":0.25, "2":0.25, "3":0.25}, 3)   # example with 3 qubits
        {'000': 0.25, '001': 0.25, '010': 0.25, '011': 0.25}
        ```
    """
    if num_qubits <= 0:
        raise ValueError("Number of qubits must be positive")
    _check_states_in_range(probabilities, num_qubits)
    result = {}
    for state, probability in probabilities.items():
        result[format(int(state), f"0{num_qubits}b")] = probability
    return result


def marginal(probabilities: Mapping[str, float], qubits: Sequence[int], num_qubits: int) -> dict[str, float]:
    """Compute the marginal probabilities over a subset of qubits.

    Qubit indices follow the module convention: qubit i is bit 2^i
    in the integer state key.  The output keys are new integers where the
    selected qubits are packed in the order given by ``qubits`` --
    ``qubits[0]`` becomes the most significant bit of the output key.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        qubits: Qubit indices to keep.  The order matters: ``qubits[0]`` maps
            to the highest bit in the output key.
        num_qubits: Total number of qubits in the original state.

    Returns:
        Mapping from integer state keys (as strings) to marginal probabilities.

    Raises:
        ValueError: If ``qubits`` is empty, has duplicate or negative indices,
            or indexes past ``num_qubits``; if ``num_qubits`` is not positive;
            or if a state key does not fit in ``num_qubits`` qubits.

    Examples:
        ```python
        >>> marginal({"0": 0.1, "1":0.2, "2":0.3, "3":0.4}, [0], 2)   # keep qubit 0 (bit 2^0)
        {'0': 0.4, '1': 0.6}
        >>> marginal({"0": 0.1, "1":0.2, "2":0.3, "3":0.4}, [1,0], 2)   # keep both, q1 q0 order
        {'0': 0.1, '1': 0.2, '2': 0.3, '3': 0.4}
        >>> marginal({"0": 0.1, "1":0.2, "2":0.3, "3":0.4}, [0,1], 2)   # keep both, q0 q1 order (swapped)
        {'0': 0.1, '1': 0.3, '2': 0.2, '3': 0.4}
        ```
    """
    if not qubits:
        raise ValueError("Qubits sequence cannot be empty")
    if min(qubits) < 0:
        raise ValueError("Qubit indices must be non-negative")
    if num_qubits <= 0:
        raise ValueError("Number of qubits must be positive")
    _check_states_in_range(probabilities, num_qubits)
    if max(qubits) >= num_qubits:
        raise ValueError("Qubit indices must be less than the number of qubits")
    if len(set(qubits)) != len(qubits):
        raise ValueError("Qubit indices must be unique")
    result = defaultdict(float)
    for state_string, probability in probabilities.items():
        state = int(state_string)
        marginalized_state = 0
        for qubit in qubits:
            marginalized_state = (marginalized_state << 1) + ((state >> qubit) & 1)
        result[str(marginalized_state)] += probability

    return dict(result)


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Calculate the expectation value of the all-qubit parity observable (Z on every qubit).

    Each computational basis state contributes +1 when the total number of
    qubits in |1> is even, and -1 when odd.  This is independent of qubit
    ordering.

    Args:
        probabilities: Mapping from integer state keys (as strings) to probabilities.
        num_qubits: Total number of qubits.

    Returns:
        Expectation value observed in the computational basis (Z basis).

    Raises:
        ValueError: If ``num_qubits`` is not positive, or a state key does not
            fit in ``num_qubits`` qubits.

    Examples:
        ```python
        >>> expectation_z({"0": 0.1, "1":0.2, "2":0.3, "3":0.4}, 2)   # even-parity states: 0,3; odd-parity: 1,2
        0.0
        ```
    """
    if num_qubits <= 0:
        raise ValueError("Number of qubits must be positive")
    _check_states_in_range(probabilities, num_qubits)
    result = 0.0
    for state, probability in probabilities.items():
        result += (1 - 2 * (int(state).bit_count() & 1)) * probability
    return result


def _check_states_in_range(probabilities: Mapping[str, float], num_qubits: int) -> None:
    """Raise if any integer state key does not fit in ``num_qubits`` qubits."""
    if not probabilities:
        return
    max_state = max(int(state) for state in probabilities)
    if max_state >= (1 << num_qubits):
        raise ValueError(f"State {max_state} is out of range for {num_qubits} qubits")
