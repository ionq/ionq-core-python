# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python helpers for post-processing IonQ probability results.

The probability endpoints (`get_job_probabilities`, `get_variant_probabilities`,
`get_variant_histogram`) return a sparse mapping from measured basis state to
probability, exposed as `GetResultsResponse.additional_properties`. Each key is
the **integer encoding of the measured bitstring**, as a string, so `int(key)`
parses it. The helpers here operate on that plain `Mapping[str, float]`, so they
work for both the job and variant endpoints and are testable without HTTP.

Bit-ordering convention
-----------------------
IonQ encodes state keys **big-endian**: qubit ``0`` is the *most* significant
bit of the integer, and the last measured qubit is the least significant bit.
So for an ``n``-qubit register the integer ``key`` corresponds to the bitstring
``format(key, f"0{n}b")``, read left-to-right as qubits ``0, 1, ..., n - 1``.
For example, on three qubits the integer ``2`` is ``"010"`` -- qubit ``1`` is
the only one measured in state ``1``. Every helper below follows this
convention.

This module is intentionally NumPy-free (`math` and the standard library only),
matching `ionq_core.gates`.

Example:
    ```python
    from ionq_core import probabilities_to_counts, expectation_z
    from ionq_core.api.default import get_job_probabilities

    probs = get_job_probabilities.sync(uuid, client=client).additional_properties
    probabilities_to_counts(probs, shots=1000)  # {"0": 500, "3": 500}
    expectation_z(probs, num_qubits=2)  # 1.0 for a Bell state
    ```
"""

from __future__ import annotations

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

import math
from collections.abc import Iterable, Mapping


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert a probability mapping to integer shot counts.

    Counts are assigned with the largest-remainder method, so they always sum
    exactly to ``shots`` even when ``probability * shots`` is fractional. Ties on
    the fractional remainder are broken by ascending integer state value, keeping
    the result deterministic.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
            Probabilities must be finite and non-negative and sum to 1 within a
            small floating-point tolerance.
        shots: Number of shots to distribute. Must be non-negative.

    Returns:
        A mapping with the same keys as ``probabilities`` and integer counts that
        sum to ``shots``.

    Raises:
        ValueError: If ``shots`` is negative, a probability is invalid, the
            probabilities do not sum to 1, or the mapping is empty while
            ``shots`` is positive.
    """
    if shots < 0:
        raise ValueError("shots must be non-negative")

    floors: dict[str, int] = {}
    remainders: list[tuple[float, int, str]] = []
    total = 0.0
    for key, probability in probabilities.items():
        probability = _validate_probability(probability, key)
        total += probability
        state = _parse_state_key(key)
        exact = probability * shots
        floor = math.floor(exact)
        floors[key] = floor
        remainders.append((exact - floor, state, key))

    if not floors:
        if shots == 0:
            return {}
        raise ValueError("probabilities must not be empty when shots is positive")

    if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("probabilities must sum to 1")

    leftover = shots - sum(floors.values())
    for _, _, key in sorted(remainders, key=lambda item: (-item[0], item[1]))[:leftover]:
        floors[key] += 1
    return floors


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys to zero-padded big-endian bitstrings.

    The bitstring is read left-to-right as qubits ``0, 1, ..., num_qubits - 1``
    (qubit ``0`` most significant), matching IonQ's wire convention.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        num_qubits: Width of the measured register; must be at least 1.

    Returns:
        A mapping from ``num_qubits``-wide bitstrings to probabilities.

    Raises:
        ValueError: If ``num_qubits`` is less than 1, or a state key is not an
            integer within the register, or a probability is invalid.
    """
    _validate_num_qubits(num_qubits)
    relabeled: dict[str, float] = {}
    for key, probability in probabilities.items():
        probability = _validate_probability(probability, key)
        state = _parse_state_key(key, num_qubits)
        relabeled[format(state, f"0{num_qubits}b")] = probability
    return relabeled


def marginal(probabilities: Mapping[str, float], qubits: Iterable[int], num_qubits: int) -> dict[str, float]:
    """Marginalize the distribution onto a subset of qubits.

    Probability mass is summed over the qubits that are dropped. Result keys are
    integer-encoded over the kept qubits, in the order given by ``qubits``: the
    first entry of ``qubits`` becomes the most significant bit of the reduced
    key, consistent with the big-endian convention used throughout this module.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        qubits: Qubit indices to keep, in output order. Must be distinct and
            within ``range(num_qubits)``.
        num_qubits: Width of the full measured register; must be at least 1.

    Returns:
        A probability mapping over the kept qubits, keyed by integer-encoded
        reduced state.

    Raises:
        ValueError: If ``num_qubits`` is less than 1, a kept qubit is out of
            range or repeated, a state key is invalid, or a probability is
            invalid.
    """
    kept = _normalize_qubits(qubits, num_qubits)
    reduced: dict[str, float] = {}
    for key, probability in probabilities.items():
        probability = _validate_probability(probability, key)
        state = _parse_state_key(key, num_qubits)
        reduced_key = str(_project_state(state, kept, num_qubits))
        reduced[reduced_key] = reduced.get(reduced_key, 0.0) + probability
    return reduced


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the all-qubit Pauli-``Z`` parity expectation value.

    Returns ``Sum_x p(x) * (-1) ** popcount(x)`` -- the expectation of
    ``Z ⊗ Z ⊗ ... ⊗ Z`` over every measured qubit. The result lies in
    ``[-1, 1]``; a Bell state gives ``1.0``.

    Args:
        probabilities: Mapping from integer-encoded state keys to probabilities.
        num_qubits: Width of the measured register; must be at least 1.

    Returns:
        The parity expectation value.

    Raises:
        ValueError: If ``num_qubits`` is less than 1, a state key is invalid, or
            a probability is invalid.
    """
    _validate_num_qubits(num_qubits)
    expectation = 0.0
    for key, probability in probabilities.items():
        probability = _validate_probability(probability, key)
        state = _parse_state_key(key, num_qubits)
        expectation += probability if state.bit_count() % 2 == 0 else -probability
    return expectation


def _normalize_qubits(qubits: Iterable[int], num_qubits: int) -> tuple[int, ...]:
    _validate_num_qubits(num_qubits)
    kept = tuple(qubits)
    seen: set[int] = set()
    for qubit in kept:
        if qubit < 0 or qubit >= num_qubits:
            raise ValueError(f"qubit {qubit} is outside the {num_qubits}-qubit register")
        if qubit in seen:
            raise ValueError(f"qubit {qubit} is repeated")
        seen.add(qubit)
    return kept


def _project_state(state: int, qubits: tuple[int, ...], num_qubits: int) -> int:
    reduced = 0
    for output_index, qubit in enumerate(qubits):
        bit = (state >> (num_qubits - 1 - qubit)) & 1
        reduced |= bit << (len(qubits) - 1 - output_index)
    return reduced


def _parse_state_key(key: str, num_qubits: int | None = None) -> int:
    try:
        state = int(key)
    except ValueError as exc:
        raise ValueError(f"state key {key!r} is not an integer") from exc
    if state < 0:
        raise ValueError(f"state key {key!r} must be non-negative")
    if num_qubits is not None and state >= 1 << num_qubits:
        raise ValueError(f"state key {key!r} is outside the {num_qubits}-qubit register")
    return state


def _validate_num_qubits(num_qubits: int) -> None:
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")


def _validate_probability(probability: float, key: str) -> float:
    if not math.isfinite(probability):
        raise ValueError(f"probability for state key {key!r} must be finite")
    if probability < 0:
        raise ValueError(f"probability for state key {key!r} must be non-negative")
    return probability
