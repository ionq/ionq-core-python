# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

import pytest

from ionq_core import expectation_z, marginal, probabilities_to_counts, relabel_to_bitstrings

FIXTURES = Path(__file__).parent / "fixtures"
BELL_PROBABILITIES = json.loads((FIXTURES / "bell_probabilities.json").read_text())


class TestProbabilitiesToCounts:
    def test_bell_state_counts_sum_to_shots(self):
        assert probabilities_to_counts(BELL_PROBABILITIES, 1000) == {"0": 500, "3": 500}

    def test_largest_remainder_rounding_is_stable(self):
        assert probabilities_to_counts({"0": 0.333, "1": 0.333, "2": 0.334}, 10) == {"0": 3, "1": 3, "2": 4}

    def test_zero_shots_returns_zero_counts(self):
        assert probabilities_to_counts(BELL_PROBABILITIES, 0) == {"0": 0, "3": 0}

    def test_negative_shots_raise(self):
        with pytest.raises(ValueError, match="shots"):
            probabilities_to_counts(BELL_PROBABILITIES, -1)


class TestRelabelToBitstrings:
    def test_bell_state_integer_keys_become_zero_padded_bitstrings(self):
        assert relabel_to_bitstrings(BELL_PROBABILITIES, 2) == {"00": 0.5, "11": 0.5}

    def test_state_keys_must_fit_num_qubits(self):
        with pytest.raises(ValueError, match="fit"):
            relabel_to_bitstrings({"4": 1.0}, 2)

    def test_state_keys_must_be_non_negative_integers(self):
        with pytest.raises(ValueError, match="integer"):
            relabel_to_bitstrings({"not-an-int": 1.0}, 2)
        with pytest.raises(ValueError, match="non-negative"):
            relabel_to_bitstrings({"-1": 1.0}, 2)

    def test_num_qubits_must_be_non_negative(self):
        with pytest.raises(ValueError, match="num_qubits"):
            relabel_to_bitstrings({"0": 1.0}, -1)


class TestMarginal:
    def test_single_qubit_marginal_uses_little_endian_indices(self):
        assert marginal({"1": 1.0}, [0], 2) == {"1": 1.0}
        assert marginal({"1": 1.0}, [1], 2) == {"0": 1.0}

    def test_output_bitstrings_follow_requested_qubit_order(self):
        assert marginal({"1": 1.0}, [0, 1], 2) == {"10": 1.0}
        assert marginal({"1": 1.0}, [1, 0], 2) == {"01": 1.0}

    def test_bell_state_one_qubit_marginal(self):
        assert marginal(BELL_PROBABILITIES, [0], 2) == {"0": 0.5, "1": 0.5}

    def test_empty_qubit_subset_collapses_to_empty_bitstring(self):
        assert marginal(BELL_PROBABILITIES, [], 2) == {"": 1.0}

    def test_duplicate_qubits_raise(self):
        with pytest.raises(ValueError, match="duplicate"):
            marginal(BELL_PROBABILITIES, [0, 0], 2)

    def test_qubits_must_be_in_range(self):
        with pytest.raises(ValueError, match="range"):
            marginal(BELL_PROBABILITIES, [2], 2)


class TestExpectationZ:
    def test_bell_state_even_parity_expectation_is_one(self):
        assert expectation_z(BELL_PROBABILITIES, 2) == 1.0

    def test_balanced_distribution_expectation_is_zero(self):
        assert expectation_z({"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}, 2) == 0.0

    def test_odd_parity_state_expectation_is_negative_one(self):
        assert expectation_z({"1": 1.0}, 2) == -1.0
