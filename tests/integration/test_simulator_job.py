"""Integration tests for job lifecycle against the simulator."""

import pytest

from ionq_core import iter_jobs, wait_for_job
from ionq_core.api.default import (
    cancel_job,
    create_job,
    delete_job,
    estimate_job_cost,
    get_job,
    get_job_cost,
    get_job_probabilities,
    get_jobs,
)
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

pytestmark = pytest.mark.integration

BELL_CIRCUIT = {
    "type": "ionq.circuit.v1",
    "backend": "simulator",
    "shots": 100,
    "input": {
        "gateset": "qis",
        "circuit": [
            {"gate": "h", "targets": [0]},
            {"gate": "cnot", "control": 0, "target": 1},
        ],
    },
}


class TestCreateJob:
    def test_create_returns_id(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        resp = create_job.sync_detailed(client=client, body=body)
        assert resp.status_code.value == 201
        assert resp.parsed is not None
        track_job(resp.parsed.id)
        assert resp.parsed.status == "submitted"

    def test_create_dry_run(self, client, track_job):
        payload = {**BELL_CIRCUIT, "dry_run": True}
        body = CircuitJobCreationPayload.from_dict(payload)
        result = create_job.sync(client=client, body=body)
        assert result is not None
        track_job(result.id)


class TestGetJob:
    def test_get_job_fields(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        created = create_job.sync(client=client, body=body)
        track_job(created.id)

        job = get_job.sync(uuid=created.id, client=client)
        assert job is not None
        assert job.id == created.id
        assert job.backend == "simulator"
        assert job.type_ == "ionq.circuit.v1"
        assert job.dry_run is False
        assert job.submitter_id
        assert job.project_id is not None

    def test_nullable_fields_on_new_job(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        created = create_job.sync(client=client, body=body)
        track_job(created.id)

        job = get_job.sync(uuid=created.id, client=client)
        assert job.failure is None
        assert job.session_id is None
        assert job.parent_job_id is None


class TestListJobs:
    def test_list_jobs(self, client):
        resp = get_jobs.sync(client=client, limit=3)
        assert resp is not None
        assert len(resp.jobs) > 0

    def test_list_jobs_with_status_filter(self, client):
        resp = get_jobs.sync(client=client, status="completed", limit=2)
        assert resp is not None
        for j in resp.jobs:
            assert j.status == "completed"

    def test_iter_jobs_pagination(self, client):
        jobs = [j for _, j in zip(range(3), iter_jobs(client, limit=1))]
        assert len(jobs) == 3
        assert len({j.id for j in jobs}) == 3


class TestSubmitAndPoll:
    def test_submit_and_poll(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        created = create_job.sync(client=client, body=body)
        track_job(created.id)

        completed = wait_for_job(client, created.id, timeout=120)
        assert completed.status == "completed"
        assert completed.execution_duration_ms is not None
        assert completed.started_at is not None
        assert completed.completed_at is not None


class TestCompletedJobEndpoints:
    """Tests that use an already-completed job to avoid simulator timeout."""

    @pytest.fixture
    def completed_job_id(self, client):
        resp = get_jobs.sync(client=client, status="completed", limit=1)
        assert resp is not None and resp.jobs, "No completed jobs found"
        return resp.jobs[0].id

    def test_get_job_cost(self, client, completed_job_id):
        cost = get_job_cost.sync(uuid=completed_job_id, client=client)
        assert cost is not None
        assert cost.cost is not None

    def test_get_job_probabilities(self, client, completed_job_id):
        probs = get_job_probabilities.sync(uuid=completed_job_id, client=client)
        assert probs is not None
        assert len(probs.additional_properties) > 0
        for state, prob in probs.additional_properties.items():
            assert isinstance(prob, float)
            assert 0.0 <= prob <= 1.0

    def test_get_completed_job_fields(self, client, completed_job_id):
        job = get_job.sync(uuid=completed_job_id, client=client)
        assert job.status == "completed"
        assert job.results is not None
        assert job.settings is not None
        assert job.stats is not None
        assert job.output is not None
        assert job.started_at is not None
        assert job.completed_at is not None


class TestCancelJob:
    def test_cancel_submitted_job(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        created = create_job.sync(client=client, body=body)
        track_job(created.id)

        result = cancel_job.sync(uuid=created.id, client=client)
        assert result is not None


class TestDeleteJob:
    def test_delete_job(self, client):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        created = create_job.sync(client=client, body=body)

        result = delete_job.sync(uuid=created.id, client=client)
        assert result is not None


class TestEstimateJobCost:
    def test_estimate_qpu(self, client):
        result = estimate_job_cost.sync(
            client=client,
            backend="qpu.forte-1",
            qubits=2,
            shots=1000,
            field_1q_gates=1,
            field_2q_gates=1,
        )
        assert result is not None
