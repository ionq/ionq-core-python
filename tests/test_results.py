import pytest

from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings

BELL_PROBABILITIES = {"0": 0.5, "3": 0.5}


def test_probabilities_to_counts_uses_largest_remainder_rounding():
    assert probabilities_to_counts({"0": 0.333, "1": 0.333, "2": 0.334}, 10) == {
        "0": 3,
        "1": 3,
        "2": 4,
    }


def test_probabilities_to_counts_breaks_ties_by_integer_state():
    assert probabilities_to_counts({"3": 0.25, "2": 0.25, "1": 0.25, "0": 0.25}, 2) == {
        "3": 0,
        "2": 0,
        "1": 1,
        "0": 1,
    }


def test_probabilities_to_counts_returns_exact_integer_counts_for_bell_state():
    counts = probabilities_to_counts(BELL_PROBABILITIES, 101)

    assert counts == {"0": 51, "3": 50}
    assert sum(counts.values()) == 101


def test_probabilities_to_counts_returns_floor_counts_without_remainder():
    assert probabilities_to_counts(BELL_PROBABILITIES, 100) == {"0": 50, "3": 50}


def test_probabilities_to_counts_rejects_negative_shots():
    with pytest.raises(ValueError, match="shots must be non-negative"):
        probabilities_to_counts(BELL_PROBABILITIES, -1)


def test_probabilities_to_counts_rejects_probabilities_too_large():
    with pytest.raises(ValueError, match="probabilities must sum"):
        probabilities_to_counts({"0": 0.75, "1": 0.75}, 10)


def test_probabilities_to_counts_rejects_probabilities_too_small():
    with pytest.raises(ValueError, match="probabilities must sum"):
        probabilities_to_counts({"0": 0.1, "1": 0.1}, 10)


def test_relabel_to_bitstrings_zero_pads_integer_state_keys():
    assert relabel_to_bitstrings({"0": 0.5, "1": 0.25, "5": 0.25}, 3) == {
        "000": 0.5,
        "001": 0.25,
        "101": 0.25,
    }


def test_relabel_to_bitstrings_rejects_negative_num_qubits():
    with pytest.raises(ValueError, match="num_qubits must be non-negative"):
        relabel_to_bitstrings(BELL_PROBABILITIES, -1)


def test_relabel_to_bitstrings_rejects_state_outside_register():
    with pytest.raises(ValueError, match="does not fit"):
        relabel_to_bitstrings({"4": 1.0}, 2)


def test_marginal_keeps_requested_qubit_order():
    probabilities = {"0": 0.1, "1": 0.2, "4": 0.3, "5": 0.4}

    assert marginal(probabilities, [0, 2], 3) == {
        "00": 0.1,
        "10": 0.2,
        "01": 0.3,
        "11": 0.4,
    }


def test_marginal_combines_probability_mass():
    assert marginal(BELL_PROBABILITIES, [0], 2) == {"0": 0.5, "1": 0.5}


def test_marginal_over_no_qubits_returns_total_probability():
    assert marginal(BELL_PROBABILITIES, [], 2) == {"": 1.0}


def test_marginal_rejects_duplicate_qubits():
    with pytest.raises(ValueError, match="duplicates"):
        marginal(BELL_PROBABILITIES, [0, 0], 2)


def test_marginal_rejects_qubit_outside_register():
    with pytest.raises(ValueError, match="outside the range"):
        marginal(BELL_PROBABILITIES, [2], 2)


def test_expectation_z_for_bell_state_is_one():
    assert expectation_z(BELL_PROBABILITIES, 2) == 1.0


def test_expectation_z_uses_parity_sign():
    assert expectation_z({"0": 0.1, "1": 0.2, "2": 0.3, "3": 0.4}, 2) == pytest.approx(0.0)


def test_expectation_z_rejects_state_outside_register():
    with pytest.raises(ValueError, match="does not fit"):
        expectation_z({"8": 1.0}, 3)
