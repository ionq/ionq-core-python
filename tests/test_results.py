import pytest

from ionq_core.results import (
    expectation_z,
    marginal,
    probabilities_to_counts,
    relabel_to_bitstrings,
)


@pytest.fixture
def bell_probabilities():
    return {"0": 0.5, "3": 0.5}


class TestProbabilitiesToCounts:
    def test_bell_counts(self, bell_probabilities):
        probabilities = bell_probabilities
        shots = 100
        expected = {"0": 50, "3": 50}

        counts = probabilities_to_counts(probabilities, shots)

        assert counts == expected
        assert sum(counts.values()) == shots

    def test_remainder_rounding(self):
        probabilities = {"0": 0.333, "1": 0.333, "2": 0.334}
        shots = 10
        expected = {"2": 4, "0": 3, "1": 3}

        counts = probabilities_to_counts(probabilities, shots)

        assert counts == expected
        assert sum(counts.values()) == shots

    def test_tie_breaking(self):
        probabilities = {"0": 0.25, "1": 0.25, "2": 0.25, "3": 0.25}
        shots = 50
        expected = {"0": 13, "1": 13, "2": 12, "3": 12}

        counts = probabilities_to_counts(probabilities, shots)

        assert counts == expected
        assert sum(counts.values()) == shots

    def test_zero_shots(self, bell_probabilities):
        probabilities = bell_probabilities
        shots = 0
        expected = {"0": 0, "3": 0}

        assert probabilities_to_counts(probabilities, shots) == expected

    def test_negative_shots(self, bell_probabilities):
        probabilities = bell_probabilities
        shots = -1

        with pytest.raises(ValueError, match="Number of shots cannot be negative"):
            probabilities_to_counts(probabilities, shots)


class TestRelabelToBitstrings:
    def test_bell_bitstrings(self, bell_probabilities):
        probabilities = bell_probabilities
        num_qubits = 2
        expected = {"00": 0.5, "11": 0.5}

        assert relabel_to_bitstrings(probabilities, num_qubits) == expected

    def test_zero_padding(self):
        probabilities = {"1": 0.25, "4": 0.75}
        num_qubits = 3
        expected = {"001": 0.25, "100": 0.75}

        assert relabel_to_bitstrings(probabilities, num_qubits) == expected

    def test_negative_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        num_qubits = -1

        with pytest.raises(ValueError, match="Number of qubits cannot be negative"):
            relabel_to_bitstrings(probabilities, num_qubits)


class TestMarginal:
    def test_bell_marginal(self, bell_probabilities):
        probabilities = bell_probabilities
        num_qubits = 2
        expected = {"0": 0.5, "1": 0.5}

        assert marginal(probabilities, [0], num_qubits) == expected
        assert marginal(probabilities, [1], num_qubits) == expected

    def test_three_qubit_subset(self):
        probabilities = {
            "0": 0.05,
            "1": 0.10,
            "2": 0.15,
            "3": 0.20,
            "4": 0.10,
            "5": 0.15,
            "6": 0.10,
            "7": 0.15,
        }
        qubits = [0, 2]
        num_qubits = 3
        expected = {"0": 0.20, "1": 0.30, "2": 0.20, "3": 0.30}

        assert marginal(probabilities, qubits, num_qubits) == pytest.approx(expected)

    def test_qubit_order(self):
        probabilities = {"2": 1.0}
        num_qubits = 2
        high_then_low = {"1": 1.0}
        low_then_high = {"2": 1.0}

        assert marginal(probabilities, [1, 0], num_qubits) == high_then_low
        assert marginal(probabilities, [0, 1], num_qubits) == low_then_high

    def test_empty_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = []
        num_qubits = 2
        expected = {"0": 1.0}

        assert marginal(probabilities, qubits, num_qubits) == expected

    def test_negative_num_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = [0]
        num_qubits = -1

        with pytest.raises(ValueError, match="Number of qubits cannot be negative"):
            marginal(probabilities, qubits, num_qubits)

    def test_too_many_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = [0, 1, 2]
        num_qubits = 2

        with pytest.raises(ValueError, match="Cannot select more qubits than the number of qubits"):
            marginal(probabilities, qubits, num_qubits)

    def test_qubit_outside_range(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = [2]
        num_qubits = 2

        with pytest.raises(ValueError, match="Qubit index is outside the valid range"):
            marginal(probabilities, qubits, num_qubits)

    def test_negative_qubit(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = [-1]
        num_qubits = 2

        with pytest.raises(ValueError, match="Qubit index is outside the valid range"):
            marginal(probabilities, qubits, num_qubits)

    def test_duplicate_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        qubits = [0, 0]
        num_qubits = 2

        with pytest.raises(ValueError, match="Qubits cannot contain duplicates"):
            marginal(probabilities, qubits, num_qubits)


class TestExpectationZ:
    def test_bell_expectation(self, bell_probabilities):
        probabilities = bell_probabilities
        num_qubits = 2
        expected = 1.0

        assert expectation_z(probabilities, num_qubits) == expected

    def test_mixed_parity(self):
        probabilities = {"0": 0.2, "1": 0.2, "2": 0.25, "3": 0.35}
        num_qubits = 2
        expected = 0.10

        assert expectation_z(probabilities, num_qubits) == pytest.approx(expected)

    def test_negative_num_qubits(self, bell_probabilities):
        probabilities = bell_probabilities
        num_qubits = -1

        with pytest.raises(ValueError, match="Number of qubits cannot be negative"):
            expectation_z(probabilities, num_qubits)
