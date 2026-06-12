# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for IonQ result probabilities.

IonQ result endpoints return mappings from integer-encoded state keys to
probabilities. For example, a two-qubit Bell state appears as
``{"0": 0.5, "3": 0.5}``.

**Bit-ordering convention:**

- State keys are parsed as integers with qubit 0 in the least-significant bit.

Example:
    ```python
    probabilities_to_counts({"0": 0.5, "3": 0.5}, 100)  # {"0": 50, "3": 50}
    relabel_to_bitstrings({"0": 0.5, "3": 0.5}, 2)  # {"00": 0.5, "11": 0.5}
    marginal({"0": 0.5, "3": 0.5}, [0], 2)  # {"0": 0.5, "1": 0.5}
    expectation_z({"0": 0.5, "3": 0.5}, 2)  # 1.0
    ```
"""

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

import math
from collections.abc import Mapping, Sequence


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert result probabilities to integer shot counts.

    Counts are rounded with the largest-remainder method so they sum exactly to
    ``shots``.

    Args:
        probabilities: Mapping from IonQ integer state keys, as strings, to
            probabilities.
        shots: Total number of shots to distribute.

    Returns:
        A mapping over the same state keys with integer counts.

    Raises:
        ValueError: If ``shots`` is negative.

    Examples:
        ```python
        >>> probabilities_to_counts({"0": 0.5, "3": 0.5}, 100)
        {'0': 50, '3': 50}
        >>> probabilities_to_counts({"0": 0.333, "1": 0.333, "2": 0.334}, 10)
        {'2': 4, '0': 3, '1': 3}
        ```
    """
    if shots < 0:
        raise ValueError("Number of shots cannot be negative")

    intermediate: list[tuple[str, int, float]] = []
    total = 0

    for state_key, probability in probabilities.items():
        count = probability * shots
        floor_count = math.floor(count)
        remainder = count - floor_count

        intermediate.append((state_key, floor_count, remainder))
        total += floor_count

    remaining = shots - total

    intermediate.sort(key=lambda x: (-x[2], int(x[0])))

    for index in range(remaining):
        state_key, count, remainder = intermediate[index]
        intermediate[index] = (state_key, count + 1, remainder)

    result: dict[str, int] = {}
    for state_key, count, _ in intermediate:
        result[state_key] = count

    return result


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys as zero-padded bitstrings.

    Probabilities are copied unchanged.

    Args:
        probabilities: Mapping from IonQ integer state keys, as strings, to
            probabilities.
        num_qubits: Number of measured qubits.

    Returns:
        A mapping from zero-padded bitstring keys to probabilities.

    Raises:
        ValueError: If ``num_qubits`` is negative.

    Examples:
        ```python
        >>> relabel_to_bitstrings({"0": 0.5, "3": 0.5}, 2)
        {'00': 0.5, '11': 0.5}
        >>> relabel_to_bitstrings({"1": 1.0}, 3)
        {'001': 1.0}
        ```
    """
    if num_qubits < 0:
        raise ValueError("Number of qubits cannot be negative")

    result = {}

    for state_key, probability in probabilities.items():
        state = int(state_key)
        bitstring = format(state, f"0{num_qubits}b")
        result[bitstring] = probability

    return result


def marginal(probabilities: Mapping[str, float], qubits: Sequence[int], num_qubits: int) -> dict[str, float]:
    """Marginalize a probability distribution over selected qubits.

    Full-register states that match on the selected qubits are grouped together
    and their probabilities are added.

    Args:
        probabilities: Mapping from IonQ integer state keys, as strings, to
            probabilities.
        qubits: Qubit indices to keep. Qubit 0 is the rightmost bit of the
            full-register bitstring.
        num_qubits: Number of measured qubits in the input distribution.

    Returns:
        A probability mapping over the selected qubits, using IonQ integer
        state keys encoded as strings.

    Raises:
        ValueError: If ``num_qubits`` is negative, if more qubits are selected
            than exist in the input distribution, or if a selected qubit index
            is outside the valid range, or if a selected qubit is repeated.

    Examples:
        ```python
        >>> marginal({"0": 0.1, "1": 0.2, "2": 0.3, "3": 0.4}, [0], 2)
        {'0': 0.4, '1': 0.6}
        >>> marginal({"0": 0.5, "3": 0.5}, [0], 2)
        {'0': 0.5, '1': 0.5}
        ```
    """
    if num_qubits < 0:
        raise ValueError("Number of qubits cannot be negative")

    if len(qubits) > num_qubits:
        raise ValueError("Cannot select more qubits than the number of qubits")

    for qubit in qubits:
        if qubit < 0 or qubit >= num_qubits:
            raise ValueError("Qubit index is outside the valid range")

    if len(set(qubits)) != len(qubits):
        raise ValueError("Qubits cannot contain duplicates")

    bitstring_probs = relabel_to_bitstrings(probabilities, num_qubits)

    result = {}

    for bitstring, prob in bitstring_probs.items():
        new_bits = ""

        for qubit in qubits:
            # Qubit 0 is the rightmost bit of the displayed bitstring.
            new_bits = bitstring[num_qubits - 1 - qubit] + new_bits

        key = str(int(new_bits, 2)) if new_bits else "0"

        result[key] = result.get(key, 0.0) + prob

    return result


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the full-register Pauli Z expectation value.

    States with an even number of ``1`` bits contribute positively; states with
    an odd number of ``1`` bits contribute negatively.

    Args:
        probabilities: Mapping from IonQ integer state keys, as strings, to
            probabilities.
        num_qubits: Number of measured qubits.

    Returns:
        The expectation value of ``Z...Z``.

    Raises:
        ValueError: If ``num_qubits`` is negative.

    Examples:
        ```python
        >>> expectation_z({"0": 0.5, "3": 0.5}, 2)
        1.0
        >>> expectation_z({"0": 0.5, "1": 0.5}, 1)
        0.0
        ```
    """
    if num_qubits < 0:
        raise ValueError("Number of qubits cannot be negative")

    total = 0.0
    for state_key, probability in probabilities.items():
        state = int(state_key)

        if state.bit_count() % 2:
            total -= probability
        else:
            total += probability

    return total
