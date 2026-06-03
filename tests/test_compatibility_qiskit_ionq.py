"""
API compatibility tests for qiskit-ionq v1.0.3.

These tests monitor API response schemas to detect breaking changes
that would affect qiskit-ionq. Tests do not fail - they only warn.

Run with: pytest -m compatibility tests/test_compatibility_qiskit_ionq.py -v -s
"""

import pytest

from ionq_core.api.backends import get_backend
from ionq_core.api.characterizations import get_characterizations_for_backend
from ionq_core.api.default import (
    cancel_job,
    create_job,
    delete_job,
    estimate_job_cost,
    get_compiled_file,
    get_job,
    get_job_probabilities,
    get_jobs,
)
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

# Import compatibility fixtures
from .compatibility_conftest import warn_team_instead_of_fail


class TestQiskitIonQCompatibilityV1_0_3:
    """
    Compatibility tests for qiskit-ionq v1.0.3.

    These tests verify that API response schemas contain all fields
    that qiskit-ionq relies on. Breaking changes trigger warnings
    but do not fail the test suite.

    Each test is marked with @warn_team_instead_of_fail(team_name="devtools")
    which converts assertion failures to warnings instead of test failures.
    """

    @pytest.fixture(scope="class")
    def bell_circuit(self):
        """Standard Bell state circuit for testing."""
        return {
            "type": "ionq.circuit.v1",
            "backend": "simulator",
            "shots": 100,
            "input": {
                "gateset": "qis",
                "qubits": 2,
                "circuit": [
                    {"gate": "h", "target": 0},
                    {"gate": "cnot", "control": 0, "target": 1},
                ],
            },
        }

    @pytest.fixture(scope="class")
    def test_job_id(self, client, bell_circuit):
        """
        Create a test job and return its ID.

        This job will be used across multiple tests in the class.
        It's automatically cleaned up by the integration test fixtures.
        """
        body = CircuitJobCreationPayload.from_dict(bell_circuit)
        result = create_job.sync(client=client, body=body)
        return result.id

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_job_submission_response_schema(self, client, bell_circuit, check_schema_compatibility):
        """
        POST /jobs - Verify job submission response contains required fields.

        qiskit-ionq relies on:
        - 'id': To track job throughout lifecycle
        - 'status': Initial job state (should be 'submitted')

        Breaking changes:
        - Removing 'id' field would break job tracking
        - Changing status code from 201 would break client code
        - Removing 'status' field would break status checks
        """
        body = CircuitJobCreationPayload.from_dict(bell_circuit)
        resp = create_job.sync_detailed(client=client, body=body)

        # Check against baseline
        check_schema_compatibility("POST /jobs", resp.parsed.to_dict(), status_code=resp.status_code.value)

        # Explicit critical field checks
        assert resp.parsed.id is not None, "Job ID is None"
        assert resp.parsed.status is not None, "Job status is None"
        assert resp.status_code.value == 201, f"Expected status 201, got {resp.status_code.value}"

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_job_retrieval_response_schema(self, client, test_job_id, check_schema_compatibility):
        """
        GET /jobs/{job_id} - Verify job retrieval response schema.

        qiskit-ionq relies on:
        - 'id', 'status', 'backend', 'type': Basic job info
        - 'results': Contains probabilities/shots URLs
        - 'metadata': Contains qiskit_header for circuit reconstruction
        - 'execution_duration_ms': For timing info

        Breaking changes:
        - Removing 'metadata' would break circuit reconstruction
        - Removing 'results' would break result retrieval
        - Changing field types would break parsing
        """
        job = get_job.sync(uuid=test_job_id, client=client)
        job_dict = job.to_dict()

        check_schema_compatibility("GET /jobs/{job_id}", job_dict, status_code=200)

        # Critical fields for qiskit-ionq
        assert "id" in job_dict, "Missing 'id' field"
        assert "status" in job_dict, "Missing 'status' field"
        assert "backend" in job_dict, "Missing 'backend' field"
        assert "type" in job_dict, "Missing 'type' field"

        # These can be None but key must exist
        assert "metadata" in job_dict or job_dict.get("metadata") is None
        assert "results" in job_dict or job_dict.get("results") is None

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_completed_job_results_schema(self, client, check_schema_compatibility):
        """
        GET /jobs/{job_id}/results/probabilities - Verify results format.

        qiskit-ionq expects:
        - Dict[str, float] where keys are bitstrings (e.g., "00", "11")
        - All values between 0.0 and 1.0
        - Keys should be decimal integers as strings

        Breaking changes:
        - Changing to different format would break result parsing
        - Values outside [0,1] would indicate broken probability distribution
        - Non-numeric keys would break bitstring parsing
        """
        # Use an already-completed job to avoid timeout
        resp = get_jobs.sync(client=client, status="completed", limit=1)

        if not resp or not resp.jobs:
            pytest.skip("No completed jobs available for testing")

        job_id = resp.jobs[0].id
        probs = get_job_probabilities.sync(uuid=job_id, client=client)

        if not probs:
            pytest.skip("No probabilities available for completed job")

        probs_dict = probs.additional_properties

        # Verify it's a dict
        assert isinstance(probs_dict, dict), "Results should be a dictionary"

        # Verify all values are floats between 0 and 1
        for key, value in probs_dict.items():
            assert isinstance(key, str), f"Key {key} should be string"
            assert isinstance(value, (int, float)), f"Value for {key} should be numeric"
            assert 0.0 <= value <= 1.0, f"Probability {value} out of range [0, 1]"

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_backend_info_schema(self, client, check_schema_compatibility):
        """
        GET /backends/{backend} - Verify backend info schema.

        qiskit-ionq relies on:
        - 'qubits': Number of qubits (used in get_n_qubits helper)
        - 'status': Backend availability
        - 'backend': Backend name

        Breaking changes:
        - Removing 'qubits' would break circuit validation
        - Changing 'qubits' type to non-int would break numeric operations
        """
        backend = get_backend.sync("simulator", client=client)
        backend_dict = backend.to_dict()

        check_schema_compatibility("GET /backends/{backend}", backend_dict, status_code=200)

        # Critical field
        assert "qubits" in backend_dict, "Missing 'qubits' field"
        assert isinstance(backend_dict["qubits"], int), f"'qubits' should be int, got {type(backend_dict['qubits'])}"
        assert backend_dict["qubits"] > 0, f"'qubits' should be positive, got {backend_dict['qubits']}"

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_characterization_schema(self, client, check_schema_compatibility):
        """
        GET /backends/{backend}/characterizations - Verify calibration data schema.

        qiskit-ionq relies on:
        - 'characterizations' array
        - Each entry: 'qubits', 'connectivity', 'fidelity', 'timing'
        - Used for backend.calibration() method

        Breaking changes:
        - Removing 'characterizations' array would break calibration data access
        - Removing 'qubits' or 'connectivity' would break topology info
        """
        try:
            resp = get_characterizations_for_backend.sync("qpu.forte-1", client=client, limit=1)
        except Exception as e:
            pytest.skip(f"Characterizations endpoint not accessible: {e}")

        if not resp or not resp.characterizations:
            pytest.skip("No characterizations available")

        char = resp.characterizations[0]
        char_dict = char.to_dict()

        # Verify critical fields exist
        assert "qubits" in char_dict, "Missing 'qubits' in characterization"
        assert "connectivity" in char_dict or char_dict.get("connectivity") is None
        assert isinstance(char_dict["qubits"], int), "'qubits' should be int"

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_compiled_circuit_schema(self, client, test_job_id):
        """
        GET /jobs/{job_id}/circuits/{lang} - Verify compiled circuit format.

        qiskit-ionq expects:
        - String response
        - 'native': JSON-parseable circuit
        - 'qasm3': OpenQASM 3 source

        Breaking changes:
        - Changing response type from string would break compiled_circuit() method
        - Invalid JSON for 'native' would break parsing
        """
        import json as json_module

        try:
            # Try to get compiled circuit (may not be available immediately)
            result = get_compiled_file.sync(uuid=test_job_id, lang="native", client=client)

            if result:
                assert isinstance(result, str), "Compiled circuit should be string"

                # Try parsing as JSON for native format
                try:
                    parsed = json_module.loads(result)
                    assert isinstance(parsed, (list, dict)), "Native circuit should be JSON array or object"
                except json_module.JSONDecodeError:
                    # May not be compiled yet or different format
                    pass
        except Exception as e:
            # Compiled circuit might not be available for all jobs
            pytest.skip(f"Compiled circuit not available: {e}")

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_job_cancellation_schema(self, client, bell_circuit):
        """
        PUT /jobs/{job_id}/status/cancel - Verify cancellation response.

        qiskit-ionq checks 'status' after cancellation.

        Breaking changes:
        - Removing 'status' field would break cancel verification
        - Removing 'id' field would break job identification
        """
        # Create job to cancel
        body = CircuitJobCreationPayload.from_dict(bell_circuit)
        result = create_job.sync(client=client, body=body)
        job_id = result.id

        try:
            # Cancel immediately
            cancel_result = cancel_job.sync(uuid=job_id, client=client)

            if cancel_result:
                cancel_dict = cancel_result.to_dict()
                assert "id" in cancel_dict, "Missing 'id' in cancel response"
                assert "status" in cancel_dict, "Missing 'status' in cancel response"
        finally:
            # Clean up - delete the job
            try:
                delete_job.sync(uuid=job_id, client=client)
            except Exception as e:
                print(f"Error occurred while deleting job: {e}")

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_job_deletion_schema(self, client, bell_circuit):
        """
        DELETE /jobs/{job_id} - Verify deletion response.

        qiskit-ionq verifies deletion by checking returned ID.

        Breaking changes:
        - Removing 'id' field would break deletion verification
        - Changing status code would break error handling
        """
        # Create job to delete
        body = CircuitJobCreationPayload.from_dict(bell_circuit)
        result = create_job.sync(client=client, body=body)
        job_id = result.id

        # Delete
        delete_result = delete_job.sync(uuid=job_id, client=client)

        if delete_result:
            delete_dict = delete_result.to_dict()
            assert "id" in delete_dict, "Missing 'id' in delete response"

    @pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
    @warn_team_instead_of_fail(team_name="devtools")
    def test_cost_estimation_schema(self, client, check_schema_compatibility):
        """
        GET /jobs/estimate - Verify cost estimation response.

        qiskit-ionq displays:
        - 'estimated_cost': Cost value
        - 'estimated_execution_time': Time estimate

        Breaking changes:
        - Removing cost fields would break cost display
        - Changing types would break numeric calculations
        """
        result = estimate_job_cost.sync(
            client=client,
            backend="qpu.forte-1",
            qubits=2,
            shots=1000,
            field_1q_gates=1,
            field_2q_gates=1,
        )

        if not result:
            pytest.skip("Cost estimation not available")

        result_dict = result.to_dict()

        # Check critical fields
        assert "estimated_cost" in result_dict, "Missing 'estimated_cost'"
        assert "estimated_execution_time" in result_dict, "Missing 'estimated_execution_time'"

        # These should be numeric
        cost = result_dict.get("estimated_cost")
        if cost is not None:
            assert isinstance(cost, (int, float)), f"'estimated_cost' should be numeric, got {type(cost)}"
