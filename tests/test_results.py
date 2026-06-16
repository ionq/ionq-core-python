# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Tests for ionq_core.results."""

from __future__ import annotations

import math

import pytest

from ionq_core.results import (
    expectation_z,
    marginal,
    probabilities_to_counts,
    relabel_to_bitstrings,
)

BELL = {"0": 0.5, "3": 0.5}


# ── probabilities_to_counts ──────────────────────────────────────────


class TestProbabilitiesToCounts:
    def test_round_numbers(self):
        """Even split gives exact integer counts."""
        assert probabilities_to_counts(BELL, 1000) == {"0": 500, "3": 500}

    def test_largest_remainder(self):
        c = probabilities_to_counts({"0": 0.333, "1": 0.333, "2": 0.334}, 1000)
        assert c["2"] == 334
        assert sum(c.values()) == 1000

    def test_tied_remainder(self):
        c = probabilities_to_counts({"0": 0.5, "1": 0.5}, 1, drop_zeros=False)
        assert sorted(c.values()) == [0, 1]

    def test_empty_or_zero_shots(self):
        assert probabilities_to_counts({}, 1000) == {}
        assert probabilities_to_counts(BELL, 0) == {}

    def test_negative_shots(self):
        with pytest.raises(ValueError, match="shots must be non-negative"):
            probabilities_to_counts(BELL, -1)

    def test_drop_zeros_false(self):
        c = probabilities_to_counts({"0": 1.0}, 100, drop_zeros=False)
        assert "0" in c and c["0"] == 100

    def test_invalid_probability(self):
        with pytest.raises(ValueError, match=r"finite and non.negative"):
            probabilities_to_counts({"0": math.nan}, 100)
        with pytest.raises(ValueError, match=r"finite and non.negative"):
            probabilities_to_counts({"0": math.inf}, 100)
        with pytest.raises(ValueError, match=r"finite and non.negative"):
            probabilities_to_counts({"0": -0.1}, 100)


# ── relabel_to_bitstrings ────────────────────────────────────────────


class TestRelabelToBitstrings:
    def test_bell_state(self):
        assert relabel_to_bitstrings(BELL, 2) == {"00": 0.5, "11": 0.5}

    def test_three_qubits(self):
        assert relabel_to_bitstrings({"0": 0.25, "5": 0.75}, 3) == {
            "000": 0.25,
            "101": 0.75,
        }

    def test_little_endian(self):
        """qubit 0 appears on the left when little_endian=True."""
        assert relabel_to_bitstrings({"1": 1.0}, 2, little_endian=True) == {"10": 1.0}

    def test_little_endian_bell(self):
        """Bell state: key 3 (0b11) → '11' either way (symmetric)."""
        assert relabel_to_bitstrings(BELL, 2, little_endian=True) == {"00": 0.5, "11": 0.5}

    def test_out_of_bounds(self):
        with pytest.raises(ValueError, match="out of bounds"):
            relabel_to_bitstrings({"4": 1.0}, 2)


# ── marginal ─────────────────────────────────────────────────────────


class TestMarginal:
    def test_bell_single_qubit(self):
        assert marginal(BELL, [0], 2) == {"0": 0.5, "1": 0.5}
        assert marginal(BELL, [1], 2) == {"0": 0.5, "1": 0.5}

    def test_reversed_order(self):
        assert marginal(BELL, [1, 0], 2) == {"0": 0.5, "3": 0.5}

    def test_accumulates(self):
        assert marginal({"1": 0.3, "2": 0.7}, [0], 2) == {"1": 0.3, "0": 0.7}

    def test_empty_qubits(self):
        with pytest.raises(ValueError, match="qubits must not be empty"):
            marginal(BELL, [], 2)

    def test_duplicate_qubits(self):
        with pytest.raises(ValueError, match="duplicate"):
            marginal(BELL, [0, 0], 2)

    def test_out_of_range_qubit(self):
        with pytest.raises(ValueError, match="out of bounds"):
            marginal(BELL, [2], 2)
        with pytest.raises(ValueError, match="out of bounds"):
            marginal(BELL, [-1], 2)


# ── expectation_z ────────────────────────────────────────────────────


class TestExpectationZ:
    def test_bell_state(self):
        """Both outcomes even parity → ⟨Z⟩ = +1."""
        assert expectation_z(BELL, 2) == 1.0

    def test_even_superposition(self):
        """|+⟩ → ⟨Z⟩ = 0."""
        assert expectation_z({"0": 0.5, "1": 0.5}, 1) == 0.0

    def test_pure_states(self):
        assert expectation_z({"0": 1.0}, 1) == 1.0
        assert expectation_z({"1": 1.0}, 1) == -1.0

    def test_asymmetric(self):
        assert math.isclose(expectation_z({"0": 0.3, "1": 0.7}, 1), -0.4)

    def test_all_odd_parity(self):
        """Every outcome has odd parity → ⟨Z⟩ = -1."""
        assert expectation_z({"1": 0.4, "2": 0.6}, 2) == -1.0

    def test_out_of_bounds(self):
        with pytest.raises(ValueError, match="out of bounds"):
            expectation_z({"4": 1.0}, 2)
