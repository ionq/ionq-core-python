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
    @pytest.mark.parametrize(
        ("probabilities", "shots", "expected"),
        [
            ({"0": 0.4, "3": 0.6}, 100, {"0": 40, "3": 60}),
            ({"0": 0.496, "3": 0.504}, 100, {"0": 50, "3": 50}),
            ({"0": 0.251, "1": 0.243, "2": 0.254, "3": 0.252}, 100, {"0": 25, "1": 24, "2": 26, "3": 25}),
            ({"0": 0.328, "1": 0.332, "2": 0.139, "3": 0.191}, 100, {"0": 33, "1": 34, "2": 14, "3": 19}),
            ({"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}, 50, {"0": 13, "1": 13, "2": 12, "3": 12}),
            ({}, 100, {}),
            ({"0": 0.5, "3": 0.5}, 0, {"0": 0, "3": 0}),
        ],
    )
    def test_counts(self, probabilities, shots, expected):
        assert probabilities_to_counts(probabilities, shots) == expected

    def test_negative_shots(self):
        with pytest.raises(ValueError, match="Number of shots must be non-negative"):
            probabilities_to_counts({"0": 0.5, "3": 0.5}, -1)


class TestRelabelToBitstrings:
    @pytest.mark.parametrize(
        ("probabilities", "num_qubits", "expected"),
        [
            ({"1": 0.4, "2": 0.6}, 2, {"01": 0.4, "10": 0.6}),
            ({"1": 0.4, "2": 0.6}, 3, {"001": 0.4, "010": 0.6}),
            ({}, 3, {}),
        ],
    )
    def test_relabel(self, probabilities, num_qubits, expected):
        _approx(relabel_to_bitstrings(probabilities, num_qubits), expected)

    @pytest.mark.parametrize(
        ("num_qubits", "match"),
        [
            (1, "State 2 is out of range for 1 qubits"),
            (-1, "Number of qubits must be positive"),
        ],
    )
    def test_invalid(self, num_qubits, match):
        with pytest.raises(ValueError, match=match):
            relabel_to_bitstrings({"1": 0.4, "2": 0.6}, num_qubits)


class TestMarginal:
    @pytest.mark.parametrize(
        ("probabilities", "qubits", "num_qubits", "expected"),
        [
            ({"0": 0.4, "3": 0.6}, [0], 2, {"0": 0.4, "1": 0.6}),
            ({"0": 0.1, "1": 0.2, "2": 0.3, "3": 0.4}, [0], 2, {"0": 0.4, "1": 0.6}),
            ({"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}, [1, 0], 3, {"0": 0.4, "2": 0.2, "3": 0.4}),
            ({"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}, [0, 1], 3, {"0": 0.4, "1": 0.2, "3": 0.4}),
            ({}, [0], 1, {}),
        ],
    )
    def test_marginal(self, probabilities, qubits, num_qubits, expected):
        _approx(marginal(probabilities, qubits, num_qubits), expected)

    @pytest.mark.parametrize(
        ("qubits", "num_qubits", "match"),
        [
            ([0], -1, "Number of qubits must be positive"),
            ([0], 1, "State 3 is out of range for 1 qubits"),
            ([2], 2, "Qubit indices must be less than the number of qubits"),
            ([-1], 2, "Qubit indices must be non-negative"),
            ([0, 0], 2, "Qubit indices must be unique"),
            ([], 2, "Qubits sequence cannot be empty"),
        ],
    )
    def test_invalid(self, qubits, num_qubits, match):
        with pytest.raises(ValueError, match=match):
            marginal({"0": 0.4, "3": 0.6}, qubits, num_qubits)


class TestExpectationZ:
    @pytest.mark.parametrize(
        ("probabilities", "num_qubits", "expected"),
        [
            ({"0": 0.4, "3": 0.6}, 2, 1.0),
            ({"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}, 2, 0.0),
            ({"0": 0.1, "2": 0.2, "4": 0.3, "7": 0.4}, 3, -0.8),
            ({}, 2, 0.0),
        ],
    )
    def test_expectation(self, probabilities, num_qubits, expected):
        assert abs(expectation_z(probabilities, num_qubits) - expected) < TOLERANCE

    @pytest.mark.parametrize(
        ("num_qubits", "match"),
        [
            (1, "State 3 is out of range for 1 qubits"),
            (-1, "Number of qubits must be positive"),
        ],
    )
    def test_invalid(self, num_qubits, match):
        with pytest.raises(ValueError, match=match):
            expectation_z({"0": 0.4, "3": 0.6}, num_qubits)
