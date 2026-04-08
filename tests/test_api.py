import pytest

from ionq_core.api.backends import get_backends
from ionq_core.api.default import create_job, get_jobs
from ionq_core.api.whoami import get_whoami
from ionq_core.errors import UnexpectedStatus
from ionq_core.models.backend import Backend
from ionq_core.models.get_jobs_response import GetJobsResponse
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.whoami import Whoami


class TestGetWhoami:
    WHOAMI = {"key_id": "e060759f-4348-4767-a645-8c0301265791", "key_name": "Test Key"}

    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=self.WHOAMI)
        result = get_whoami.sync(client=auth_client)
        assert isinstance(result, Whoami)
        assert result.key_name == "Test Key"

    def test_sync_detailed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=self.WHOAMI)
        response = get_whoami.sync_detailed(client=auth_client)
        assert response.status_code.value == 200
        assert response.parsed.key_name == "Test Key"

    @pytest.mark.asyncio
    async def test_asyncio(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=self.WHOAMI)
        result = await get_whoami.asyncio(client=auth_client)
        assert isinstance(result, Whoami)
        assert result.key_name == "Test Key"


class TestGetBackends:
    BACKENDS_RESPONSE = [
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

    def test_sync(self, httpx_mock, client):
        httpx_mock.add_response(json=self.BACKENDS_RESPONSE)
        result = get_backends.sync(client=client)
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Backend)
        assert result[0].backend == "qpu.aria-1"
        assert result[1].degraded is True


class TestGetJobs:
    JOBS_RESPONSE = {
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

    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=self.JOBS_RESPONSE)
        result = get_jobs.sync(client=auth_client)
        assert isinstance(result, GetJobsResponse)
        assert len(result.jobs) == 1
        assert result.jobs[0].id == "job-1"
        assert result.jobs[0].status == "completed"


class TestCreateJob:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            status_code=201,
            json={"id": "new-job-id", "status": "submitted", "session_id": None},
        )
        from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

        body = CircuitJobCreationPayload.from_dict({
            "type": "ionq.circuit.v1",
            "backend": "simulator",
            "shots": 100,
            "input": {
                "gateset": "qis",
                "circuit": [{"type": "h", "targets": [0]}],
            },
        })
        result = create_job.sync(client=auth_client, body=body)
        assert isinstance(result, JobCreationResponse)
        assert result.id == "new-job-id"
        assert result.status == "submitted"


class TestUnexpectedStatus:
    def test_returns_none_by_default(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=418, content=b"teapot")
        result = get_whoami.sync(client=auth_client)
        assert result is None

    def test_raises_when_configured(self, httpx_mock, auth_client):
        auth_client.raise_on_unexpected_status = True
        httpx_mock.add_response(status_code=418, content=b"teapot")
        with pytest.raises(UnexpectedStatus) as exc_info:
            get_whoami.sync(client=auth_client)
        assert exc_info.value.status_code == 418
