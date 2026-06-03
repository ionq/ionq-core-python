"""
Compatibility testing fixtures and decorators.

This module provides infrastructure for API compatibility monitoring tests
that warn on breaking changes without failing the test suite.
"""

import functools
import json
import warnings
from collections.abc import Callable
from pathlib import Path

import pytest


class CompatibilityWarning(UserWarning):
    """Warning category for API compatibility issues."""

    pass


def warn_team_instead_of_fail(team_name: str) -> Callable:
    """
    Decorator factory that catches AssertionErrors and converts them to warnings.

    Allows compatibility tests to detect breaking changes without failing
    the test suite. Prints warning with version, endpoint_user, and team context.

    Usage:
        @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
        @warn_team_instead_of_fail(team_name="devtools")
        def test_response_schema(self, ...):
            assert "required_field" in response

    The decorator will:
    1. Try to run the test normally
    2. If AssertionError occurs, print formatted warning to stdout
    3. Issue Python warning for test runners that capture warnings
    4. Skip the test (mark as passed) instead of failing

    Args:
        team_name: Name of the team to notify on failure

    Returns:
        Decorator function that wraps test functions
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract test context from pytest markers
            # This is set by pytest_collection_modifyitems hook below
            test_obj = args[0] if args else None
            version = getattr(test_obj, "_compatibility_version", "unknown")
            endpoint_user = getattr(test_obj, "_compatibility_endpoint_user", "unknown")

            try:
                return func(*args, **kwargs)
            except AssertionError as e:
                # Format warning message for stdout
                warning_msg = (
                    f"\n{'=' * 70}\n"
                    f"API COMPATIBILITY WARNING\n"
                    f"{'=' * 70}\n"
                    f"Team: {team_name}\n"
                    f"Endpoint User: {endpoint_user}\n"
                    f"Version: {version}\n"
                    f"Test: {func.__name__}\n"
                    f"Issue: {e!s}\n"
                    f"{'=' * 70}\n"
                )

                # Print to stdout (visible in test output)
                print(warning_msg)

                # Also issue Python warning for test runners that capture warnings
                warnings.warn(
                    f"[{team_name}] [{endpoint_user} v{version}] {func.__name__}: {e}",
                    CompatibilityWarning,
                    stacklevel=2,
                )

                # Skip test instead of failing - we only want to warn
                pytest.skip(f"Compatibility issue detected: {e}")

        return wrapper

    return decorator


@pytest.fixture(scope="session")
def compatibility_baseline():
    """
    Load compatibility baseline JSON for schema comparison.

    Returns:
        dict: Parsed baseline containing endpoint schemas

    Raises:
        pytest.skip: If baseline file not found
    """
    baseline_path = Path(__file__).parent / "compatibility_baselines" / "qiskit_ionq_v1.0.3.json"

    if not baseline_path.exists():
        pytest.skip(f"Baseline file not found: {baseline_path}")

    with open(baseline_path) as f:
        return json.load(f)


@pytest.fixture
def check_schema_compatibility(compatibility_baseline):
    """
    Fixture providing schema compatibility checking function.

    Returns a callable that compares actual API responses against
    the baseline schema expectations.

    Usage:
        def test_endpoint(check_schema_compatibility):
            response = api_call()
            check_schema_compatibility("POST /jobs", response, status_code=201)

    Returns:
        Callable[[str, dict, int], None]: Schema checker function
    """

    def _check(endpoint: str, actual_response: dict, status_code: int = 200):
        """
        Compare actual response against baseline schema.

        Args:
            endpoint: API endpoint identifier (e.g., "POST /jobs")
            actual_response: Actual API response dict
            status_code: Actual HTTP status code

        Raises:
            AssertionError: If breaking change detected
            UserWarning: If baseline not found for endpoint
        """
        baseline = compatibility_baseline["endpoints"].get(endpoint)
        if not baseline:
            warnings.warn(f"No baseline found for endpoint: {endpoint}", CompatibilityWarning, stacklevel=1)
            return

        schema = baseline["response_schema"]

        # Check status code
        expected_status = schema.get("status_code")
        if expected_status is not None:
            assert status_code == expected_status, f"Status code changed: expected {expected_status}, got {status_code}"

        # Check required fields exist
        required = schema.get("required_fields", [])
        for field in required:
            assert field in actual_response, f"Required field '{field}' missing from response"

        # Check critical fields (those qiskit-ionq actually uses)
        critical = baseline.get("critical_fields", [])
        for field_path in critical:
            if field_path == "*":
                # Wildcard - all fields are critical, just verify response exists
                continue

            # Support nested field paths like "metadata.qiskit_header"
            parts = field_path.split(".")
            current = actual_response

            for part in parts:
                # Handle array notation like "characterizations[]"
                if part.endswith("[]"):
                    part = part[:-2]
                    assert isinstance(current.get(part), list), f"Field '{field_path}' should be a list"
                    if current[part]:  # Check first element if list non-empty
                        current = current[part][0]
                    else:
                        break  # Empty list, can't check nested fields
                else:
                    assert part in current, f"Critical field '{field_path}' missing from response"
                    current = current.get(part)
                    if current is None:
                        break  # Null value, can't check nested fields

        # Check field types for critical fields
        field_types = schema.get("field_types", {})
        for field, expected_type in field_types.items():
            if field not in actual_response:
                # Field not present - may be nullable
                continue

            actual_value = actual_response[field]

            # Handle nullable types like "string|null"
            allowed_types = expected_type.split("|")
            type_map = {
                "string": str,
                "integer": int,
                "float": float,
                "boolean": bool,
                "object": dict,
                "array": list,
                "null": type(None),
            }

            type_matches = any(isinstance(actual_value, type_map[t]) for t in allowed_types if t in type_map)

            assert type_matches, (
                f"Field '{field}' type mismatch: expected {expected_type}, got {type(actual_value).__name__}"
            )

    return _check


def pytest_configure(config):
    """Register compatibility marker with pytest."""
    config.addinivalue_line("markers", "compatibility(version, endpoint_user): mark test as API compatibility check")


def pytest_collection_modifyitems(config, items):
    """
    Inject version and endpoint_user into test instances from markers.

    This hook runs during test collection and extracts the version and
    endpoint_user parameters from @pytest.mark.compatibility markers,
    storing them on the test instance for access by @warn_team_on_fail.

    Args:
        config: Pytest config object
        items: List of collected test items
    """
    for item in items:
        marker = item.get_closest_marker("compatibility")
        if marker:
            version = marker.kwargs.get("version", "unknown")
            endpoint_user = marker.kwargs.get("endpoint_user", "unknown")

            # Store in test instance for decorator access
            if hasattr(item, "instance") and item.instance:
                item.instance._compatibility_version = version
                item.instance._compatibility_endpoint_user = endpoint_user
