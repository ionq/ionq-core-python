"""Integration tests for job lifecycle against the simulator."""

import itertools

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
        "qubits": 2,
        "circuit": [
            {"gate": "h", "target": 0},
            {"gate": "cnot", "control": 0, "target": 1},
        ],
    },
}


def _submit(client, **overrides):
    body = CircuitJobCreationPayload.from_dict({**BELL_CIRCUIT, **overrides})
    result = create_job.sync(client=client, body=body)
    assert result is not None, "create_job returned None"
    return result


class TestCreateJob:
    def test_create_returns_id(self, client, track_job):
        body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
        resp = create_job.sync_detailed(client=client, body=body)
        assert resp.status_code.value == 201
        assert resp.parsed is not None
        track_job(resp.parsed.id)
        assert resp.parsed.status == "submitted"

    def test_create_dry_run(self, client, track_job):
        result = _submit(client, dry_run=True)
        track_job(result.id)


class TestGetJob:
    @pytest.fixture
    def new_job(self, client, track_job):
        created = _submit(client)
        track_job(created.id)
        return get_job.sync(uuid=created.id, client=client)

    def test_fields(self, new_job):
        assert new_job.backend == "simulator"
        assert new_job.type_ == "ionq.circuit.v1"
        assert new_job.dry_run is False
        assert new_job.submitter_id
        assert new_job.project_id is not None

    def test_nullable_fields(self, new_job):
        assert new_job.failure is None
        assert new_job.session_id is None
        assert new_job.parent_job_id is None


class TestListJobs:
    def test_list_jobs(self, client):
        resp = get_jobs.sync(client=client, limit=3)
        assert resp is not None
        assert len(resp.jobs) > 0

    def test_status_filter(self, client):
        resp = get_jobs.sync(client=client, status="completed", limit=2)
        assert resp is not None
        for j in resp.jobs:
            assert j.status == "completed"

    def test_pagination(self, client):
        jobs = list(itertools.islice(iter_jobs(client, limit=1), 3))
        assert len(jobs) == 3
        assert len({j.id for j in jobs}) == 3


def test_submit_and_poll(client, track_job):
    created = _submit(client)
    track_job(created.id)

    completed = wait_for_job(client, created.id, timeout=120)
    assert completed.status == "completed"
    assert completed.execution_duration_ms is not None
    assert completed.started_at is not None
    assert completed.completed_at is not None


@pytest.fixture(scope="session")
def completed_job_id(self, client):
    resp = get_jobs.sync(client=client, status="completed", limit=1)
    assert resp is not None and resp.jobs, "No completed jobs found"
    return resp.jobs[0].id


class TestCompletedJobEndpoints:
    """Use an already-completed job to avoid simulator timeout."""

    def test_get_job_cost(self, client, completed_job_id):
        cost = get_job_cost.sync(uuid=completed_job_id, client=client)
        assert cost is not None
        assert cost.cost is not None

    def test_get_job_probabilities(self, client, completed_job_id):
        probs = get_job_probabilities.sync(uuid=completed_job_id, client=client)
        assert probs is not None
        assert len(probs.additional_properties) > 0
        for prob in probs.additional_properties.values():
            assert 0.0 <= prob <= 1.0

    def test_completed_job_fields(self, client, completed_job_id):
        job = get_job.sync(uuid=completed_job_id, client=client)
        assert job.status == "completed"
        assert job.results is not None
        assert job.settings is not None
        assert job.stats is not None
        assert job.output is not None
        assert job.started_at is not None
        assert job.completed_at is not None


def test_cancel_job(client, track_job):
    created = _submit(client)
    track_job(created.id)
    result = cancel_job.sync(uuid=created.id, client=client)
    assert result is not None


def test_delete_job(client, track_job):
    created = _submit(client)
    track_job(created.id)
    result = delete_job.sync(uuid=created.id, client=client)
    assert result is not None


def test_estimate_job_cost(client):
    result = estimate_job_cost.sync(
        client=client,
        backend="qpu.forte-1",
        qubits=2,
        shots=1000,
        field_1q_gates=1,
        field_2q_gates=1,
    )
    assert result is not None
