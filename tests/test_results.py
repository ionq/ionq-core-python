# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

import pytest

from ionq_core.results import (
    expectation_z,
    marginal,
    probabilities_to_counts,
    relabel_to_bitstrings,
)

TOLERANCE = 1e-12


def _approx(actual, expected, tol=TOLERANCE):
    assert actual.keys() == expected.keys(), f"keys differ: {actual.keys()} != {expected.keys()}"
    for key in expected:
        assert abs(actual[key] - expected[key]) < tol, f"key {key!r}: {actual[key]} != {expected[key]}"


class TestProbabilitiesToCounts:
    def test_simple_case(self):
        probabilities = {"0": 0.4, "3": 0.6}
        shots = 100
        expected = {"0": 40, "3": 60}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_rounding_case(self):
        probabilities = {"0": 0.496, "3": 0.504}
        shots = 100
        expected = {"0": 50, "3": 50}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_multiple_rounding_case_1(self):
        probabilities = {"0": 0.251, "1": 0.243, "2": 0.254, "3": 0.252}
        shots = 100
        expected = {"0": 25, "1": 24, "2": 26, "3": 25}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_multiple_rounding_case_2(self):
        probabilities = {"0": 0.328, "1": 0.332, "2": 0.139, "3": 0.191}
        shots = 100
        expected = {"0": 33, "1": 34, "2": 14, "3": 19}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_break_even(self):
        probabilities = {"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}
        shots = 50
        expected = {"0": 13, "1": 13, "2": 12, "3": 12}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_empty_input(self):
        probabilities = {}
        shots = 100
        expected = {}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_zero_shots(self):
        probabilities = {"0": 0.5, "3": 0.5}
        shots = 0
        expected = {"0": 0, "3": 0}
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_negative_shots(self):
        probabilities = {"0": 0.5, "3": 0.5}
        shots = -1
        with pytest.raises(ValueError, match=r"Number of shots must be non-negative."):
            probabilities_to_counts(probabilities, shots)


class TestRelabelToBitstrings:
    def test_simple_case(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = 2
        expected = {"01": 0.4, "10": 0.6}
        _approx(relabel_to_bitstrings(probabilities, num_qubits), expected)

    def test_simple_case_little_endian(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = 2
        expected = {"10": 0.4, "01": 0.6}
        _approx(relabel_to_bitstrings(probabilities, num_qubits, little_endian=True), expected)

    def test_more_qubits(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = 3
        expected = {"001": 0.4, "010": 0.6}
        _approx(relabel_to_bitstrings(probabilities, num_qubits), expected)

    def test_more_qubits_little_endian(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = 3
        expected = {"100": 0.4, "010": 0.6}
        _approx(relabel_to_bitstrings(probabilities, num_qubits, little_endian=True), expected)

    def test_empty_input(self):
        probabilities = {}
        num_qubits = 3
        expected = {}
        _approx(relabel_to_bitstrings(probabilities, num_qubits), expected)

    def test_out_of_range_qubits(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = 1
        with pytest.raises(ValueError, match=r"State 2 is out of range for 1 qubits."):
            relabel_to_bitstrings(probabilities, num_qubits)

    def test_negative_qubits(self):
        probabilities = {"1": 0.4, "2": 0.6}
        num_qubits = -1
        with pytest.raises(ValueError, match=r"Number of qubits must be positive."):
            relabel_to_bitstrings(probabilities, num_qubits)


class TestMarginal:
    def test_simple_case(self):
        probablities = {"0": 0.4, "3": 0.6}
        qubits = [0]
        num_qubits = 2
        expected = {"0": 0.4, "1": 0.6}
        _approx(marginal(probablities, qubits, num_qubits), expected)

    def test_simple_case_2(self):
        probabilities = {"0": 0.1, "1": 0.2, "2": 0.3, "3": 0.4}
        qubits = [0]
        num_qubits = 2
        expected = {"0": 0.4, "1": 0.6}
        _approx(marginal(probabilities, qubits, num_qubits), expected)

    def test_simple_case_3(self):
        probabilities = {"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}
        qubits = [1, 0]
        num_qubits = 3
        expected = {"0": 0.4, "2": 0.2, "3": 0.4}
        _approx(marginal(probabilities, qubits, num_qubits), expected)

    def test_reordering_qubits(self):
        probabilities = {"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}
        qubits = [0, 1]
        num_qubits = 3
        expected = {"0": 0.4, "1": 0.2, "3": 0.4}
        _approx(marginal(probabilities, qubits, num_qubits), expected)

    def test_empty_input(self):
        probabilities = {}
        qubits = [0]
        num_qubits = 1
        expected = {}
        _approx(marginal(probabilities, qubits, num_qubits), expected)

    def test_negative_qubit(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = [0]
        num_qubits = -1
        with pytest.raises(ValueError, match=r"Number of qubits must be positive."):
            marginal(probabilities, qubits, num_qubits)

    def test_out_of_range_qubit(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = [0]
        num_qubits = 1
        with pytest.raises(ValueError, match=r"State 3 is out of range for 1 qubits."):
            marginal(probabilities, qubits, num_qubits)

    def test_qubit_index_out_of_range(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = [2]
        num_qubits = 2
        with pytest.raises(ValueError, match=r"Qubit indices must be less than the number of qubits."):
            marginal(probabilities, qubits, num_qubits)

    def test_qubit_index_negative(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = [-1]
        num_qubits = 2
        with pytest.raises(ValueError, match=r"Qubit indices must be non-negative."):
            marginal(probabilities, qubits, num_qubits)

    def test_qubit_index_duplicated(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = [0, 0]
        num_qubits = 2
        with pytest.raises(ValueError, match="Qubits sequence must be non-duplicated"):
            marginal(probabilities, qubits, num_qubits)

    def test_empty_qubits(self):
        probabilities = {"0": 0.4, "3": 0.6}
        qubits = []
        num_qubits = 2
        with pytest.raises(ValueError, match=r"Qubits sequence cannot be empty."):
            marginal(probabilities, qubits, num_qubits)


class TestExpectationZ:
    def test_simple_case(self):
        probabilities = {"0": 0.4, "3": 0.6}
        num_qubits = 2
        expected = 1
        assert abs(expectation_z(probabilities, num_qubits) - expected) < TOLERANCE

    def test_simple_case_2(self):
        probabilities = {"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}
        num_qubits = 2
        expected = 0
        assert abs(expectation_z(probabilities, num_qubits) - expected) < TOLERANCE

    def test_simple_case_3(self):
        probabilities = {"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}
        num_qubits = 3
        expected = -0.8
        assert abs(expectation_z(probabilities, num_qubits) - expected) < TOLERANCE

    def test_empty_input(self):
        probabilities = {}
        num_qubits = 2
        expected = 0
        assert abs(expectation_z(probabilities, num_qubits) - expected) < TOLERANCE

    def test_qubit_out_of_range(self):
        probabilities = {"0": 0.4, "3": 0.6}
        num_qubits = 1
        with pytest.raises(ValueError, match=r"State 3 is out of range for 1 qubits."):
            expectation_z(probabilities, num_qubits)

    def test_negative_qubits(self):
        probabilities = {"0": 0.4, "3": 0.6}
        num_qubits = -1
        with pytest.raises(ValueError, match=r"Number of qubits must be positive."):
            expectation_z(probabilities, num_qubits)
