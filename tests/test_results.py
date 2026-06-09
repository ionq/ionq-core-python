import math

import pytest

import ionq_core
from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings
from ionq_core.models.get_results_response import GetResultsResponse

# Real simulator response for the two-qubit Bell circuit
# (h q0; cnot q0 q1) returned by GET /jobs/{uuid}/results/probabilities.
# Keys are big-endian integer-encoded states: "0" -> |00>, "3" -> |11>.
BELL_RESPONSE = GetResultsResponse.from_dict({"0": 0.5, "3": 0.5})
BELL_PROBABILITIES = BELL_RESPONSE.additional_properties

# Real simulator response for a three-qubit GHZ circuit
# (h q0; cnot q0 q1; cnot q1 q2): only |000> ("0") and |111> ("7") appear.
GHZ_PROBABILITIES = {"0": 0.5, "7": 0.5}


def test_helpers_reexported_from_package_root():
    assert "results" in ionq_core.__all__
    for name in ("expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"):
        assert name in ionq_core.__all__
        assert getattr(ionq_core, name) is getattr(ionq_core.results, name)


def test_relabel_bell_to_bitstrings():
    assert relabel_to_bitstrings(BELL_PROBABILITIES, 2) == {"00": 0.5, "11": 0.5}


def test_relabel_is_big_endian_qubit_zero_is_most_significant():
    # Integer 2 on three qubits is "010": only qubit 1 (the middle, big-endian) is set.
    assert relabel_to_bitstrings({"2": 1.0}, 3) == {"010": 1.0}


def test_relabel_rejects_out_of_range_state():
    with pytest.raises(ValueError, match="outside"):
        relabel_to_bitstrings({"4": 1.0}, 2)


def test_relabel_rejects_non_integer_state():
    with pytest.raises(ValueError, match="not an integer"):
        relabel_to_bitstrings({"zero": 1.0}, 2)


def test_relabel_rejects_invalid_num_qubits():
    with pytest.raises(ValueError, match="at least 1"):
        relabel_to_bitstrings(BELL_PROBABILITIES, 0)


def test_probabilities_to_counts_bell():
    counts = probabilities_to_counts(BELL_PROBABILITIES, 1000)
    assert counts == {"0": 500, "3": 500}
    assert sum(counts.values()) == 1000


def test_probabilities_to_counts_largest_remainder_distributes_leftover():
    counts = probabilities_to_counts({"0": 1 / 3, "1": 1 / 3, "2": 1 / 3}, 10)
    assert sum(counts.values()) == 10
    # All three remainders tie; ascending state value wins the single leftover.
    assert counts == {"0": 4, "1": 3, "2": 3}


def test_probabilities_to_counts_exact_when_no_remainder():
    assert probabilities_to_counts({"0": 0.2, "1": 0.3, "2": 0.5}, 10) == {"0": 2, "1": 3, "2": 5}


def test_probabilities_to_counts_zero_shots():
    assert probabilities_to_counts(BELL_PROBABILITIES, 0) == {"0": 0, "3": 0}


def test_probabilities_to_counts_empty_with_zero_shots():
    assert probabilities_to_counts({}, 0) == {}


def test_probabilities_to_counts_rejects_negative_shots():
    with pytest.raises(ValueError, match="shots must be non-negative"):
        probabilities_to_counts(BELL_PROBABILITIES, -1)


def test_probabilities_to_counts_rejects_empty_with_positive_shots():
    with pytest.raises(ValueError, match="must not be empty"):
        probabilities_to_counts({}, 100)


def test_probabilities_to_counts_rejects_non_normalized():
    with pytest.raises(ValueError, match="sum to 1"):
        probabilities_to_counts({"0": 0.4, "1": 0.5}, 100)


def test_probabilities_to_counts_rejects_non_finite_probability():
    with pytest.raises(ValueError, match="must be finite"):
        probabilities_to_counts({"0": math.inf}, 100)


def test_probabilities_to_counts_rejects_negative_probability():
    with pytest.raises(ValueError, match="must be non-negative"):
        probabilities_to_counts({"0": -0.1, "1": 1.1}, 100)


def test_probabilities_to_counts_rejects_non_integer_state():
    with pytest.raises(ValueError, match="not an integer"):
        probabilities_to_counts({"oops": 1.0}, 100)


def test_marginal_drops_qubit_and_sums_mass():
    # GHZ marginalized onto qubit 0 keeps perfect correlation: half |0>, half |1>.
    assert marginal(GHZ_PROBABILITIES, [0], 3) == {"0": 0.5, "1": 0.5}


def test_marginal_collapses_when_qubit_independent_of_state():
    # Marginalizing the Bell distribution onto qubit 0 alone: "0"->|0..>, "3"->|1..>.
    assert marginal(BELL_PROBABILITIES, [0], 2) == {"0": 0.5, "1": 0.5}


def test_marginal_respects_requested_qubit_order():
    # State "1" on three qubits is "001" (only qubit 2 set, big-endian).
    # Keeping [2, 0] big-endian: qubit 2 -> bit1, qubit 0 -> bit0 => "10" == 2.
    assert marginal({"1": 1.0}, [2, 0], 3) == {"2": 1.0}


def test_marginal_with_empty_qubit_selection_returns_total_mass():
    assert marginal(BELL_PROBABILITIES, [], 2) == {"0": 1.0}


def test_marginal_rejects_out_of_range_qubit():
    with pytest.raises(ValueError, match="outside"):
        marginal(BELL_PROBABILITIES, [2], 2)


def test_marginal_rejects_repeated_qubit():
    with pytest.raises(ValueError, match="repeated"):
        marginal(BELL_PROBABILITIES, [0, 0], 2)


def test_marginal_rejects_invalid_num_qubits():
    with pytest.raises(ValueError, match="at least 1"):
        marginal(BELL_PROBABILITIES, [0], 0)


def test_marginal_rejects_invalid_probability():
    with pytest.raises(ValueError, match="must be non-negative"):
        marginal({"0": -0.5, "1": 1.5}, [0], 1)


def test_expectation_z_bell_is_plus_one():
    assert expectation_z(BELL_PROBABILITIES, 2) == 1.0


def test_expectation_z_odd_parity_contributes_negative():
    # "1" (|01>) and "2" (|10>) have odd parity; "3" (|11>) is even.
    assert expectation_z({"1": 0.25, "2": 0.25, "3": 0.5}, 2) == 0.0


def test_expectation_z_rejects_invalid_num_qubits():
    with pytest.raises(ValueError, match="at least 1"):
        expectation_z(BELL_PROBABILITIES, 0)


def test_expectation_z_rejects_negative_state_key():
    with pytest.raises(ValueError, match="must be non-negative"):
        expectation_z({"-1": 1.0}, 2)
