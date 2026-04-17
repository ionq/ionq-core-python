import pytest

from ionq_core.api.backends import get_backends
from ionq_core.api.default import create_job, get_compiled_file, get_jobs
from ionq_core.api.whoami import get_whoami
from ionq_core.errors import UnexpectedStatus
from ionq_core.models.backend import Backend
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload
from ionq_core.models.get_jobs_response import GetJobsResponse
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.whoami import Whoami

WHOAMI_JSON = {"key_id": "e060759f-4348-4767-a645-8c0301265791", "key_name": "Test Key"}

BACKENDS_JSON = [
    {
        "backend": "qpu.aria-1",
        "status": "available",
        "degraded": False,
        "qubits": 25,
        "average_queue_time": 1181215,
        "last_updated": "2025-06-16T00:00:00Z",
    },
    {
        "backend": "qpu.forte-1",
        "status": "unavailable",
        "degraded": True,
        "qubits": 36,
        "average_queue_time": 0,
        "last_updated": "2025-06-15T00:00:00Z",
    },
]

JOBS_JSON = {
    "jobs": [
        {
            "id": "job-1",
            "status": "completed",
            "type": "ionq.circuit.v1",
            "backend": "simulator",
            "dry_run": False,
            "submitter_id": "user-1",
            "project_id": "proj-1",
            "parent_job_id": "parent-1",
            "session_id": "sess-1",
            "metadata": {},
            "name": "Test",
            "submitted_at": "2025-05-28T20:47:05.440Z",
            "started_at": "2025-05-28T20:48:00Z",
            "completed_at": "2025-05-28T20:49:00Z",
            "predicted_wait_time_ms": 5000,
            "predicted_execution_duration_ms": 3000,
            "execution_duration_ms": 2800,
            "shots": 1000,
            "failure": {"code": "InternalError", "message": "test"},
            "output": {},
            "settings": {},
            "stats": {},
            "results": {},
        }
    ],
    "next": "cursor-token",
}


class TestGetWhoami:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=WHOAMI_JSON)
        result = get_whoami.sync(client=auth_client)
        assert isinstance(result, Whoami)
        assert result.key_name == "Test Key"

    def test_sync_detailed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=WHOAMI_JSON)
        resp = get_whoami.sync_detailed(client=auth_client)
        assert resp.status_code.value == 200
        assert resp.parsed.key_name == "Test Key"

    async def test_asyncio(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=WHOAMI_JSON)
        result = await get_whoami.asyncio(client=auth_client)
        assert isinstance(result, Whoami)
        assert result.key_name == "Test Key"


class TestGetBackends:
    def test_sync(self, httpx_mock, client):
        httpx_mock.add_response(json=BACKENDS_JSON)
        result = get_backends.sync(client=client)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Backend)
        assert result[0].backend == "qpu.aria-1"
        assert result[1].degraded is True


class TestGetJobs:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=JOBS_JSON)
        result = get_jobs.sync(client=auth_client)
        assert isinstance(result, GetJobsResponse)
        assert len(result.jobs) == 1
        assert result.jobs[0].id == "job-1"
        assert result.jobs[0].status == "completed"


class TestCreateJob:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json={"id": "new-job-id", "status": "submitted", "session_id": None})
        body = CircuitJobCreationPayload.from_dict(
            {
                "type": "ionq.circuit.v1",
                "backend": "simulator",
                "shots": 100,
                "input": {"gateset": "qis", "circuit": [{"gate": "h", "targets": [0]}]},
            }
        )
        result = create_job.sync(client=auth_client, body=body)
        assert isinstance(result, JobCreationResponse)
        assert result.id == "new-job-id"
        assert result.status == "submitted"


class TestGetCompiledFile:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(json="OPENQASM 3.0;\nqubit[2] q;\nh q[0];\ncx q[0], q[1];")
        result = get_compiled_file.sync(uuid="job-123", lang="qasm3", client=auth_client)
        assert isinstance(result, str)
        assert "OPENQASM" in result

    def test_sync_detailed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json="compiled-native-circuit")
        resp = get_compiled_file.sync_detailed(uuid="job-123", lang="native", client=auth_client)
        assert resp.status_code.value == 200
        assert resp.parsed == "compiled-native-circuit"

    async def test_asyncio(self, httpx_mock, auth_client):
        httpx_mock.add_response(json="OPENQASM 3.0;\nh q[0];")
        result = await get_compiled_file.asyncio(uuid="job-123", lang="qasm3", client=auth_client)
        assert isinstance(result, str)

    def test_not_found(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=404)
        result = get_compiled_file.sync(uuid="nonexistent", lang="native", client=auth_client)
        assert result is None


class TestUnexpectedStatus:
    def test_returns_none_by_default(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=418, content=b"teapot")
        assert get_whoami.sync(client=auth_client) is None

    def test_raises_when_configured(self, httpx_mock, auth_client):
        auth_client.raise_on_unexpected_status = True
        httpx_mock.add_response(status_code=418, content=b"teapot")
        with pytest.raises(UnexpectedStatus) as exc_info:
            get_whoami.sync(client=auth_client)
        assert exc_info.value.status_code == 418
