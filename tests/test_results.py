"""
Tests for pure-Python results post-processing helpers.
"""

import math

import pytest

from ionq_core.results import (
    expectation_z,
    marginal,
    probabilities_to_counts,
    relabel_to_bitstrings,
)

# --- Fixtures ---


@pytest.fixture
def bell_state() -> dict[str, float]:
    """A standard two-qubit Bell state response."""
    return {"0": 0.5, "3": 0.5}


@pytest.fixture
def ghz_state() -> dict[str, float]:
    """A three-qubit GHZ state."""
    return {"0": 0.5, "7": 0.5}


# --- Validation Tests ---


def test_invalid_probabilities():
    """Ensure non-finite and negative probabilities are rejected."""
    with pytest.raises(ValueError, match="finite and non-negative"):
        probabilities_to_counts({"0": -0.5}, 100)

    with pytest.raises(ValueError, match="finite and non-negative"):
        probabilities_to_counts({"0": math.inf}, 100)

    with pytest.raises(ValueError, match="finite and non-negative"):
        probabilities_to_counts({"0": math.nan}, 100)


# --- probabilities_to_counts Tests ---


def test_probabilities_to_counts_bell(bell_state):
    """Test standard perfect distribution."""
    counts = probabilities_to_counts(bell_state, 100)
    assert counts == {"0": 50, "3": 50}


def test_probabilities_to_counts_rounding():
    """Test largest-remainder method with tricky fractions and deterministic tie-breaking."""
    probs = {"0": 1 / 3, "1": 1 / 3, "2": 1 / 3}
    counts = probabilities_to_counts(probs, 10)
    # Exact is 3.333 each. Base is 3, 3, 3. Shortfall is 1.
    # Tie-breaker should pick the lowest integer state ("0") to get the +1.
    assert counts == {"0": 4, "1": 3, "2": 3}
    assert sum(counts.values()) == 10


def test_probabilities_to_counts_invalid_shots(bell_state):
    with pytest.raises(ValueError, match="at least 1"):
        probabilities_to_counts(bell_state, 0)


# --- relabel_to_bitstrings Tests ---


def test_relabel_to_bitstrings_bell(bell_state):
    result = relabel_to_bitstrings(bell_state, 2)
    assert result == {"00": 0.5, "11": 0.5}


def test_relabel_to_bitstrings_invalid_qubits(bell_state):
    with pytest.raises(ValueError, match="at least 1"):
        relabel_to_bitstrings(bell_state, 0)


def test_relabel_to_bitstrings_out_of_bounds():
    with pytest.raises(ValueError, match="out of bounds"):
        relabel_to_bitstrings({"4": 1.0}, 2)


# --- marginal Tests ---


def test_marginal_bell(bell_state):
    """Marginalizing a Bell state on either qubit gives a 50/50 mix."""
    res_q0 = marginal(bell_state, [0], 2)
    assert res_q0 == {"0": 0.5, "1": 0.5}

    res_q1 = marginal(bell_state, [1], 2)
    assert res_q1 == {"0": 0.5, "1": 0.5}


def test_marginal_ghz_subset(ghz_state):
    """Extracting qubits 0 and 2 from a 3-qubit GHZ state."""
    # Qubit 0 and 2 from |000> is |00> (state 0). From |111> is |11> (state 3).
    res = marginal(ghz_state, [0, 2], 3)
    assert res == {"0": 0.5, "3": 0.5}


def test_marginal_invalid_inputs(bell_state):
    with pytest.raises(ValueError, match="at least one qubit"):
        marginal(bell_state, [], 2)

    with pytest.raises(ValueError, match="unique"):
        marginal(bell_state, [0, 0], 2)

    with pytest.raises(ValueError, match="out of bounds"):
        marginal(bell_state, [2], 2)

    with pytest.raises(ValueError, match="out of bounds"):
        marginal(bell_state, [-1], 2)


# --- expectation_z Tests ---


def test_expectation_z_bell(bell_state):
    """
    Z-parity of |00> (popcount 0) is 1.
    Z-parity of |11> (popcount 2) is 1.
    Total expectation: 0.5*1 + 0.5*1 = 1.0
    """
    assert expectation_z(bell_state, 2) == 1.0


def test_expectation_z_odd_parity():
    """State '1' is '01', popcount 1 -> parity -1."""
    assert expectation_z({"1": 1.0}, 2) == -1.0


def test_expectation_z_out_of_bounds():
    with pytest.raises(ValueError, match="out of bounds"):
        expectation_z({"4": 1.0}, 2)
