# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python post-processing helpers for IonQ probability results.

The results endpoints (``get_job_probabilities``, ``get_variant_probabilities``,
``get_variant_histogram``) return IonQ's register-keyed probability mapping as-is: a
``Mapping[str, float]`` whose keys are the **decimal-integer encodings** of the measured
computational-basis states and whose values are probabilities. For a 2-qubit Bell state the
mapping looks like ``{"0": 0.5, "3": 0.5}`` (states ``|00>`` and ``|11>``).

These helpers cover the post-processing that downstream wrappers (``qiskit-ionq``,
``cirq-ionq``, ``pennylane-ionq``) would otherwise each re-implement. They are pure-Python and
NumPy-free (like :mod:`ionq_core.gates`), and operate on a plain ``Mapping[str, float]`` so they
work for both the job and variant endpoints and are testable without HTTP.

Bit-ordering convention
-----------------------
A state key is the integer ``value`` of its bitstring. Throughout this module qubit ``q`` is the
bit of weight ``2 ** (num_qubits - 1 - q)``: qubit ``0`` is the **most-significant** bit and
appears **leftmost** in the zero-padded bitstring produced by :func:`relabel_to_bitstrings`. The
same convention is used to select qubits in :func:`marginal`.

Example:
    ```python
    from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings

    probs = {"0": 0.5, "3": 0.5}  # 2-qubit Bell state
    probabilities_to_counts(probs, shots=1000)  # {"0": 500, "3": 500}
    relabel_to_bitstrings(probs, num_qubits=2)  # {"00": 0.5, "11": 0.5}
    marginal(probs, qubits=[0], num_qubits=2)  # {"0": 0.5, "1": 0.5}
    expectation_z(probs, num_qubits=2)  # 1.0
    ```
"""

__all__ = ["expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"]

from collections.abc import Mapping, Sequence


def probabilities_to_counts(probabilities: Mapping[str, float], shots: int) -> dict[str, int]:
    """Convert a probability mapping to integer shot counts summing exactly to ``shots``.

    Uses the largest-remainder (Hamilton) method: each count is first floored, then the leftover
    shots are handed out one at a time to the states with the largest fractional parts, breaking
    ties by ascending state key for determinism. The returned counts therefore sum to exactly
    ``shots`` whenever the probabilities are normalized.

    Parameters
    ----------
    probabilities : Mapping[str, float]
        State key (decimal-integer encoding) to probability.
    shots : int
        Total number of shots to distribute. Must be non-negative.

    Returns
    -------
    dict[str, int]
        State key to integer count, in the iteration order of ``probabilities``.

    Raises
    ------
    ValueError
        If ``shots`` is negative.
    """
    if shots < 0:
        raise ValueError("shots must be non-negative")
    scaled = {key: probability * shots for key, probability in probabilities.items()}
    counts = {key: int(value) for key, value in scaled.items()}
    remainder = shots - sum(counts.values())
    if remainder:
        ranked = sorted(scaled, key=lambda key: (-(scaled[key] - int(scaled[key])), key))
        for key in ranked[:remainder]:
            counts[key] += 1
    return counts


def relabel_to_bitstrings(probabilities: Mapping[str, float], num_qubits: int) -> dict[str, float]:
    """Relabel integer state keys to zero-padded bitstrings.

    Parameters
    ----------
    probabilities : Mapping[str, float]
        State key (decimal-integer encoding) to probability.
    num_qubits : int
        Number of qubits; sets the bitstring width. Must be non-negative.

    Returns
    -------
    dict[str, float]
        Zero-padded bitstring (qubit ``0`` leftmost) to probability.

    Raises
    ------
    ValueError
        If ``num_qubits`` is negative, or a state key does not fit in ``num_qubits`` qubits.
    """
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")
    bound = 1 << num_qubits
    result: dict[str, float] = {}
    for key, probability in probabilities.items():
        value = int(key)
        if not 0 <= value < bound:
            raise ValueError(f"state key {key!r} does not fit in {num_qubits} qubits")
        result[format(value, f"0{num_qubits}b")] = probability
    return result


def marginal(probabilities: Mapping[str, float], qubits: Sequence[int], num_qubits: int) -> dict[str, float]:
    """Marginalize a probability mapping over a subset of qubits.

    Probabilities are summed over all states sharing the same values on the selected ``qubits``.
    The marginal keys are bitstrings over ``qubits`` in the order given (qubit ``0`` is the
    most-significant bit of the full state; see the module docstring).

    Parameters
    ----------
    probabilities : Mapping[str, float]
        State key (decimal-integer encoding) to probability.
    qubits : Sequence[int]
        Qubits to keep, each in ``range(num_qubits)``. An empty sequence marginalizes over every
        qubit and returns ``{"": total_probability}``.
    num_qubits : int
        Total number of qubits. Must be non-negative.

    Returns
    -------
    dict[str, float]
        Sub-bitstring over ``qubits`` to summed probability.

    Raises
    ------
    ValueError
        If ``num_qubits`` is negative, a qubit is out of range, or a state key does not fit in
        ``num_qubits`` qubits.
    """
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")
    selected = list(qubits)
    for qubit in selected:
        if not 0 <= qubit < num_qubits:
            raise ValueError(f"qubit {qubit} out of range for {num_qubits} qubits")
    bound = 1 << num_qubits
    result: dict[str, float] = {}
    for key, probability in probabilities.items():
        value = int(key)
        if not 0 <= value < bound:
            raise ValueError(f"state key {key!r} does not fit in {num_qubits} qubits")
        bits = format(value, f"0{num_qubits}b")
        sub = "".join(bits[qubit] for qubit in selected)
        result[sub] = result.get(sub, 0.0) + probability
    return result


def expectation_z(probabilities: Mapping[str, float], num_qubits: int) -> float:
    """Compute the expectation value of the all-qubit Pauli-Z operator (``Z`` on every qubit).

    This is the parity sum ``sum(p(x) * (-1) ** popcount(x))``: states with an even number of set
    bits contribute ``+p`` and odd-parity states contribute ``-p``.

    Parameters
    ----------
    probabilities : Mapping[str, float]
        State key (decimal-integer encoding) to probability.
    num_qubits : int
        Number of qubits. Must be non-negative.

    Returns
    -------
    float
        The expectation value in ``[-1, 1]`` for a normalized distribution.

    Raises
    ------
    ValueError
        If ``num_qubits`` is negative, or a state key does not fit in ``num_qubits`` qubits.
    """
    if num_qubits < 0:
        raise ValueError("num_qubits must be non-negative")
    bound = 1 << num_qubits
    total = 0.0
    for key, probability in probabilities.items():
        value = int(key)
        if not 0 <= value < bound:
            raise ValueError(f"state key {key!r} does not fit in {num_qubits} qubits")
        if bin(value).count("1") % 2:
            total -= probability
        else:
            total += probability
    return total
