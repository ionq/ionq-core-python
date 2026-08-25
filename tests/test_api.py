import pytest

from ionq_core.api.backends import get_backends
from ionq_core.api.default import clone_job, create_job, get_job_artifact, get_jobs
from ionq_core.api.whoami import get_whoami
from ionq_core.errors import UnexpectedStatus
from ionq_core.models.backend import Backend
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload
from ionq_core.models.clone_job_payload import CloneJobPayload
from ionq_core.models.get_jobs_response import GetJobsResponse
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.whoami import Whoami
from tests.conftest import make_job_json

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

JOBS_JSON = {"jobs": [make_job_json("job-1")], "next": "cursor-token"}


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
                "input": {"gateset": "qis", "qubits": 1, "circuit": [{"gate": "h", "target": 0}]},
            }
        )
        result = create_job.sync(client=auth_client, body=body)
        assert isinstance(result, JobCreationResponse)
        assert result.id == "new-job-id"
        assert result.status == "submitted"


class TestGetJobArtifact:
    def test_sync_detailed(self, httpx_mock, auth_client):
        httpx_mock.add_response(content=b"OPENQASM 3.0;\nqubit[2] q;\nh q[0];\ncx q[0], q[1];")
        resp = get_job_artifact.sync_detailed(uuid="job-123", artifact_id="art-1", client=auth_client)
        assert resp.status_code.value == 200
        assert resp.parsed is None
        assert b"OPENQASM" in resp.content

    async def test_asyncio_detailed(self, httpx_mock, auth_client):
        httpx_mock.add_response(content=b"compiled-native-circuit")
        resp = await get_job_artifact.asyncio_detailed(uuid="job-123", artifact_id="art-1", client=auth_client)
        assert resp.status_code.value == 200
        assert resp.content == b"compiled-native-circuit"

    def test_not_found(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=404)
        resp = get_job_artifact.sync_detailed(uuid="nonexistent", artifact_id="art-1", client=auth_client)
        assert resp.status_code.value == 404
        assert resp.parsed is None


class TestCloneJob:
    def test_sync(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            status_code=201, json={"id": "cloned-job-id", "status": "submitted", "session_id": None}
        )
        body = CloneJobPayload.from_dict({"backend": "simulator", "shots": 100})
        result = clone_job.sync(uuid="job-123", client=auth_client, body=body)
        assert isinstance(result, JobCreationResponse)
        assert result.id == "cloned-job-id"
        assert result.status == "submitted"


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
