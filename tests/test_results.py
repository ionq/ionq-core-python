# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

import pytest

from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings

BELL_PROBABILITIES = {"0": 0.5, "3": 0.5}


def test_probabilities_to_counts_bell_state_rounds_to_exact_shots():
    assert probabilities_to_counts(BELL_PROBABILITIES, 100) == {"0": 50, "3": 50}


def test_probabilities_to_counts_uses_largest_remainder_with_stable_ties():
    probabilities = {"0": 0.333, "1": 0.333, "2": 0.334}

    assert probabilities_to_counts(probabilities, 10) == {"0": 3, "1": 3, "2": 4}
    assert probabilities_to_counts({"2": 0.5, "1": 0.5}, 1) == {"2": 0, "1": 1}


def test_probabilities_to_counts_rejects_negative_shots():
    with pytest.raises(ValueError, match="shots"):
        probabilities_to_counts(BELL_PROBABILITIES, -1)


def test_relabel_to_bitstrings_zero_pads_and_sums_duplicate_integer_labels():
    probabilities = {"0": 0.25, "01": 0.25, "3": 0.5}

    assert relabel_to_bitstrings(probabilities, 2) == {"00": 0.25, "01": 0.25, "11": 0.5}


def test_relabel_to_bitstrings_rejects_invalid_register_width():
    with pytest.raises(ValueError, match="num_qubits"):
        relabel_to_bitstrings(BELL_PROBABILITIES, -1)


def test_marginal_uses_requested_qubit_order():
    probabilities = {"0": 0.1, "1": 0.2, "4": 0.3, "5": 0.4}

    assert marginal(probabilities, [0, 2], 3) == {"00": 0.1, "10": 0.2, "01": 0.3, "11": 0.4}
    assert marginal(BELL_PROBABILITIES, [], 2) == {"": 1.0}


def test_marginal_rejects_out_of_range_qubits():
    with pytest.raises(ValueError, match="qubits"):
        marginal(BELL_PROBABILITIES, [2], 2)
    with pytest.raises(ValueError, match="qubits"):
        marginal(BELL_PROBABILITIES, [-1], 2)


def test_expectation_z_computes_all_z_parity():
    assert expectation_z(BELL_PROBABILITIES, 2) == 1.0
    assert expectation_z({"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}, 2) == 0.0


def test_helpers_reject_negative_state_keys():
    with pytest.raises(ValueError, match="state keys"):
        expectation_z({"-1": 1.0}, 1)
