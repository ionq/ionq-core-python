"""
Test the compatibility decorator behavior.

This test file verifies that @warn_team_on_fail works correctly:
1. Catching assertion failures
2. Printing warnings with version/endpoint_user context
3. Skipping tests instead of failing

Run with: pytest tests/test_compatibility_decorator.py -v -s
"""

import pytest
from .compatibility_conftest import warn_team_on_fail


@pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
class TestDecoratorBehavior:
    """Test suite to verify decorator functionality."""

    @warn_team_on_fail
    def test_passing_test_unchanged(self):
        """Passing tests should work normally."""
        assert True
        assert 1 + 1 == 2

    @warn_team_on_fail
    def test_failing_test_warns_and_skips(self):
        """Failing tests should print warning and skip."""
        # This assertion will fail
        assert False, "This is a test breaking change"

    @warn_team_on_fail
    def test_missing_field_warns(self):
        """Simulate missing field in API response."""
        response = {"id": "job-123", "status": "completed"}
        # This will fail - 'metadata' is missing
        assert "metadata" in response, "Required field 'metadata' missing from response"

    @warn_team_on_fail
    def test_type_mismatch_warns(self):
        """Simulate type change in API response."""
        response = {"qubits": "25"}  # Should be int, but is string
        assert isinstance(response["qubits"], int), (
            f"Field 'qubits' type mismatch: expected int, got {type(response['qubits']).__name__}"
        )


@pytest.mark.compatibility(version="2.0.0", endpoint_user="cirq-ionq")
class TestMultipleConsumers:
    """Verify decorator works with different version/consumer combinations."""

    @warn_team_on_fail
    def test_cirq_ionq_compatibility(self):
        """Test with different endpoint_user."""
        response = {"job_id": "123"}  # cirq-ionq expects 'job_id' not 'id'
        assert "id" in response, "cirq-ionq v2.0.0 expects 'id' field"


def test_without_decorator():
    """
    Regular test without decorator should fail normally.

    This verifies that non-compatibility tests aren't affected.
    """
    assert True  # This test should pass normally
