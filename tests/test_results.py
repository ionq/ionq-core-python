# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Tests for ionq_core.results."""

from __future__ import annotations

import math

import pytest

import ionq_core
from ionq_core.results import (
    expectation_z,
    marginal,
    probabilities_to_counts,
    relabel_to_bitstrings,
)

# A 2-qubit Bell state, as the probabilities endpoints would return it: states |00⟩ (key "0")
# and |11⟩ (key "3") with equal probability.
BELL = {"0": 0.5, "3": 0.5}

# A 3-qubit GHZ state: only |000⟩ ("0") and |111⟩ ("7") appear.
GHZ = {"0": 0.5, "7": 0.5}


# ── re-export verification ──────────────────────────────────────────


class TestReExport:
    def test_results_module_in_package_all(self):
        assert "results" in ionq_core.__all__

    def test_helpers_in_package_all(self):
        for name in ("expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"):
            assert name in ionq_core.__all__

    def test_helpers_importable_from_package_root(self):
        for name in ("expectation_z", "marginal", "probabilities_to_counts", "relabel_to_bitstrings"):
            assert getattr(ionq_core, name) is getattr(ionq_core.results, name)


# ── probabilities_to_counts ─────────────────────────────────────────


class TestProbabilitiesToCounts:
    def test_bell_state_exact_split(self):
        assert probabilities_to_counts(BELL, 1000) == {"0": 500, "3": 500}

    def test_largest_remainder_distributes_leftover(self):
        # Three equal outcomes over 10 shots: floors are 3, 3, 3 and the leftover shot goes to the
        # largest remainder (a tie here, broken by the lowest state key).
        probs = {"0": 1 / 3, "1": 1 / 3, "2": 1 / 3}
        counts = probabilities_to_counts(probs, 10)
        assert sum(counts.values()) == 10
        assert counts == {"0": 4, "1": 3, "2": 3}

    def test_tie_break_prefers_lowest_key(self):
        # Both remainders are 0.5; the single leftover shot must go to key "1", not "2".
        assert probabilities_to_counts({"2": 0.5, "1": 0.5}, 3) == {"2": 1, "1": 2}

    def test_exact_when_no_remainder(self):
        assert probabilities_to_counts({"0": 0.2, "1": 0.3, "2": 0.5}, 10) == {"0": 2, "1": 3, "2": 5}

    def test_zero_shots(self):
        assert probabilities_to_counts(BELL, 0) == {"0": 0, "3": 0}

    def test_empty_mapping(self):
        assert probabilities_to_counts({}, 100) == {}

    def test_negative_shots_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            probabilities_to_counts(BELL, -1)

    def test_non_finite_probability_raises(self):
        with pytest.raises(ValueError, match="finite and non-negative"):
            probabilities_to_counts({"0": math.nan}, 100)

    def test_infinite_probability_raises(self):
        with pytest.raises(ValueError, match="finite and non-negative"):
            probabilities_to_counts({"0": math.inf}, 100)

    def test_negative_probability_raises(self):
        with pytest.raises(ValueError, match="finite and non-negative"):
            probabilities_to_counts({"0": -0.1}, 100)


# ── relabel_to_bitstrings ───────────────────────────────────────────


class TestRelabelToBitstrings:
    def test_bell_state(self):
        assert relabel_to_bitstrings(BELL, 2) == {"00": 0.5, "11": 0.5}

    def test_zero_padding_width(self):
        assert relabel_to_bitstrings({"5": 1.0}, 4) == {"0101": 1.0}

    def test_three_qubits(self):
        assert relabel_to_bitstrings({"0": 0.25, "5": 0.75}, 3) == {"000": 0.25, "101": 0.75}

    def test_empty_mapping(self):
        assert relabel_to_bitstrings({}, 3) == {}

    def test_key_out_of_range_raises(self):
        with pytest.raises(ValueError, match="does not fit"):
            relabel_to_bitstrings({"4": 1.0}, 2)

    def test_negative_num_qubits_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            relabel_to_bitstrings(BELL, -1)


# ── marginal ────────────────────────────────────────────────────────


class TestMarginal:
    def test_single_qubit_marginal(self):
        assert marginal(BELL, [0], 2) == {"0": 0.5, "1": 0.5}

    def test_both_qubits_give_uniform(self):
        assert marginal(BELL, [1], 2) == {"0": 0.5, "1": 0.5}

    def test_accumulates_over_dropped_qubits(self):
        # Qubit 0 is 0 for both |00⟩ and |01⟩, so their probabilities are summed.
        probs = {"0": 0.25, "1": 0.25, "3": 0.5}
        assert marginal(probs, [0], 2) == {"0": 0.5, "1": 0.5}

    def test_ghz_subset(self):
        # Keeping qubits 0 and 2 from a 3-qubit GHZ state.
        res = marginal(GHZ, [0, 2], 3)
        assert res == {"00": 0.5, "11": 0.5}

    def test_reversed_order(self):
        assert marginal(BELL, [1, 0], 2) == {"00": 0.5, "11": 0.5}

    def test_empty_qubits_returns_total(self):
        assert marginal(BELL, [], 2) == {"": 1.0}

    def test_empty_probabilities(self):
        assert marginal({}, [0], 1) == {}

    def test_duplicate_qubits_raises(self):
        with pytest.raises(ValueError, match="duplicate"):
            marginal(BELL, [0, 0], 2)

    def test_qubit_out_of_range_raises(self):
        with pytest.raises(ValueError, match="out of range"):
            marginal(BELL, [2], 2)

    def test_negative_qubit_raises(self):
        with pytest.raises(ValueError, match="out of range"):
            marginal(BELL, [-1], 2)

    def test_key_out_of_range_raises(self):
        with pytest.raises(ValueError, match="does not fit"):
            marginal({"9": 1.0}, [0], 2)

    def test_negative_num_qubits_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            marginal(BELL, [0], -1)


# ── expectation_z ───────────────────────────────────────────────────


class TestExpectationZ:
    def test_bell_state_is_plus_one(self):
        assert expectation_z(BELL, 2) == pytest.approx(1.0)

    def test_odd_parity_state_is_negative(self):
        # |01⟩ (key "1") has odd parity and contributes -p.
        assert expectation_z({"1": 1.0}, 2) == pytest.approx(-1.0)

    def test_opposite_parities_cancel(self):
        assert expectation_z({"0": 0.5, "1": 0.5}, 2) == pytest.approx(0.0)

    def test_asymmetric(self):
        assert math.isclose(expectation_z({"0": 0.3, "1": 0.7}, 1), -0.4)

    def test_all_odd_parity(self):
        """Every outcome has odd parity → ⟨Z⟩ = -1."""
        assert expectation_z({"1": 0.4, "2": 0.6}, 2) == -1.0

    def test_empty_mapping_is_zero(self):
        assert expectation_z({}, 2) == 0.0

    def test_key_out_of_range_raises(self):
        with pytest.raises(ValueError, match="does not fit"):
            expectation_z({"4": 1.0}, 2)

    def test_negative_num_qubits_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            expectation_z(BELL, -1)
