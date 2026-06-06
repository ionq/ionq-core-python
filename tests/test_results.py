import math

import pytest

import ionq_core
from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings

BELL_PROBABILITIES = {"0": 0.5, "3": 0.5}


def test_results_helpers_are_reexported():
    assert "results" in ionq_core.__all__
    assert "probabilities_to_counts" in ionq_core.__all__


def test_relabel_to_bitstrings_uses_zero_padded_integer_keys():
    assert relabel_to_bitstrings(BELL_PROBABILITIES, 2) == {"00": 0.5, "11": 0.5}


def test_probabilities_to_counts_uses_largest_remainder_rounding():
    counts = probabilities_to_counts({"0": 1 / 3, "1": 1 / 3, "2": 1 / 3}, 10)

    assert counts == {"0": 4, "1": 3, "2": 3}
    assert sum(counts.values()) == 10


def test_probabilities_to_counts_keeps_exact_counts_when_no_remainder():
    assert probabilities_to_counts({"0": 0.2, "1": 0.3, "2": 0.5}, 10) == {"0": 2, "1": 3, "2": 5}


def test_probabilities_to_counts_allows_empty_zero_shots_distribution():
    assert probabilities_to_counts({}, 0) == {}


def test_probabilities_to_counts_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="shots"):
        probabilities_to_counts({"0": 1.0}, -1)

    with pytest.raises(ValueError, match="empty"):
        probabilities_to_counts({}, 1)

    with pytest.raises(ValueError, match="finite"):
        probabilities_to_counts({"0": math.inf}, 1)

    with pytest.raises(ValueError, match="non-negative"):
        probabilities_to_counts({"0": -0.1, "1": 1.1}, 1)

    with pytest.raises(ValueError, match="sum to 1"):
        probabilities_to_counts({"0": 0.4, "1": 0.5}, 10)


def test_marginal_keeps_requested_qubits_in_requested_order():
    probabilities = {"1": 0.25, "2": 0.75}

    assert marginal(BELL_PROBABILITIES, [0], 2) == {"0": 0.5, "1": 0.5}
    assert marginal(probabilities, [1, 0], 2) == {"2": 0.25, "1": 0.75}
    assert marginal(BELL_PROBABILITIES, [], 2) == {"0": 1.0}


def test_marginal_rejects_invalid_qubits():
    with pytest.raises(ValueError, match="at least 1"):
        marginal({"0": 1.0}, [0], 0)

    with pytest.raises(ValueError, match="outside"):
        marginal({"0": 1.0}, [2], 2)

    with pytest.raises(ValueError, match="repeated"):
        marginal({"0": 1.0}, [0, 0], 2)


def test_expectation_z_computes_parity_expectation():
    assert expectation_z(BELL_PROBABILITIES, 2) == 1.0
    assert expectation_z({"1": 0.25, "2": 0.25, "3": 0.5}, 2) == 0.0


def test_state_key_validation():
    with pytest.raises(ValueError, match="not an integer"):
        relabel_to_bitstrings({"zero": 1.0}, 2)

    with pytest.raises(ValueError, match="outside"):
        relabel_to_bitstrings({"4": 1.0}, 2)

    with pytest.raises(ValueError, match="outside"):
        expectation_z({"-1": 1.0}, 2)

    with pytest.raises(ValueError, match="at least 1"):
        relabel_to_bitstrings({"0": 1.0}, 0)
