"""
Pure-Python results post-processing helpers for IonQ's probability mappings.
"""

import math
from collections.abc import Mapping, Sequence

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]


def _validate_probabilities(probabilities: Mapping[str, float]) -> None:
    """Validate that all probabilities are finite and non-negative."""
    for state, prob in probabilities.items():
        if not math.isfinite(prob) or prob < 0.0:
            raise ValueError(f"Probability for state '{state}' must be finite and non-negative, got {prob}.")


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """
    Convert a probability mapping to exact integer counts summing to `shots`.

    Uses the largest-remainder method (Hare quota) to handle floating-point
    rounding errors and guarantee the final counts sum perfectly to `shots`.
    """
    if shots < 1:
        raise ValueError(f"Shots must be at least 1, got {shots}.")

    _validate_probabilities(probabilities)

    base_counts = {}
    remainders = {}

    for state, prob in probabilities.items():
        exact = prob * shots
        base = math.floor(exact)
        base_counts[state] = base
        remainders[state] = exact - base

    shortfall = shots - sum(base_counts.values())

    # Sort by remainder descending.
    # Tie-breaker: sort by integer state ascending to make it deterministic.
    sorted_states = sorted(remainders.keys(), key=lambda s: (-remainders[s], int(s)))

    counts = base_counts.copy()
    for i in range(shortfall):
        counts[sorted_states[i]] += 1

    # Only return states that actually have at least 1 count to keep the dict clean
    return {k: v for k, v in counts.items() if v > 0}


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Convert integer state keys to zero-padded big-endian bitstrings."""
    if num_qubits < 1:
        raise ValueError(f"num_qubits must be at least 1, got {num_qubits}.")

    _validate_probabilities(probabilities)
    max_state = (1 << num_qubits) - 1

    result = {}
    for state, prob in probabilities.items():
        state_int = int(state)
        if state_int < 0 or state_int > max_state:
            raise ValueError(f"State integer {state_int} is out of bounds for {num_qubits} qubits.")

        bitstring = f"{state_int:0{num_qubits}b}"
        result[bitstring] = prob

    return result


def marginal(probabilities: Mapping[str, float], qubits: Sequence[int], num_qubits: int) -> dict[str, float]:
    """
    Compute the marginal distribution over a specified subset of qubits.
    Maintains the requested order of the subset qubits in the new state keys.
    """
    if not qubits:
        raise ValueError("Must specify at least one qubit index to marginalize over.")
    if len(set(qubits)) != len(qubits):
        raise ValueError("Qubit indices must be unique.")
    for q in qubits:
        if q < 0 or q >= num_qubits:
            raise ValueError(f"Qubit index {q} is out of bounds for {num_qubits} qubits.")

    _validate_probabilities(probabilities)

    result: dict[str, float] = {}
    for state, prob in probabilities.items():
        state_int = int(state)
        new_state_int = 0

        # Extract bits big-endian style: qubit 0 is the most significant bit
        for i, q in enumerate(qubits):
            bit = (state_int >> (num_qubits - 1 - q)) & 1
            new_state_int |= bit << (len(qubits) - 1 - i)

        new_state_str = str(new_state_int)
        result[new_state_str] = result.get(new_state_str, 0.0) + prob

    return result


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """
    Calculate the Z-parity expectation value: Σ p(x)·(-1)^popcount(x).
    """
    _validate_probabilities(probabilities)
    max_state = (1 << num_qubits) - 1
    expected_value = 0.0

    for state, prob in probabilities.items():
        state_int = int(state)
        if state_int < 0 or state_int > max_state:
            raise ValueError(f"State integer {state_int} is out of bounds for {num_qubits} qubits.")

        # Z-parity is 1 if popcount is even, -1 if popcount is odd
        parity = 1 if state_int.bit_count() % 2 == 0 else -1
        expected_value += prob * parity

    return expected_value
