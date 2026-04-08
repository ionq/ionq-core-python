from uuid import UUID

from ionq_core.models.backend import Backend
from ionq_core.models.job import Job
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.session import Session
from ionq_core.models.whoami import Whoami


class TestBackendModel:
    SAMPLE = {
        "backend": "qpu.aria-1",
        "status": "available",
        "degraded": False,
        "qubits": 25,
        "average_queue_time": 1181215,
        "last_updated": "2025-06-16T00:00:00Z",
        "characterization_id": "617a1f8b-59d4-435d-aa33-695433d7155e",
        "kw": 4902.81,
        "location": "College Park, MD, USA",
    }

    def test_from_dict(self):
        backend = Backend.from_dict(self.SAMPLE)
        assert backend.backend == "qpu.aria-1"
        assert backend.status == "available"
        assert backend.degraded is False
        assert backend.qubits == 25
        assert backend.average_queue_time == 1181215
        assert backend.characterization_id == "617a1f8b-59d4-435d-aa33-695433d7155e"

    def test_round_trip(self):
        backend = Backend.from_dict(self.SAMPLE)
        result = backend.to_dict()
        assert result == self.SAMPLE


class TestJobModel:
    SAMPLE = {
        "id": "e1a09d90-b2ba-4ea5-9fd7-4bfc14eac524",
        "status": "failed",
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "dry_run": False,
        "submitter_id": "64b03577072d45001c85e9c4",
        "project_id": "1333d459-cf47-4a5e-acc1-8d4eb4f7b025",
        "parent_job_id": "parent-1",
        "session_id": "session-1",
        "metadata": {"key": "value"},
        "name": "Test Job",
        "submitted_at": "2025-05-28T20:47:05.440Z",
        "started_at": "2025-05-28T20:48:00.000Z",
        "completed_at": "2025-05-28T20:49:00.000Z",
        "predicted_wait_time_ms": 5000,
        "predicted_execution_duration_ms": 3000,
        "execution_duration_ms": 2800,
        "shots": 1000,
        "failure": {"code": "SimulationError", "message": "Test failure"},
        "output": {},
        "settings": {},
        "stats": {},
        "results": {},
    }

    def test_from_dict(self):
        job = Job.from_dict(self.SAMPLE)
        assert job.id == "e1a09d90-b2ba-4ea5-9fd7-4bfc14eac524"
        assert job.status == "failed"
        assert job.backend == "simulator"
        assert job.shots == 1000

    def test_round_trip(self):
        job = Job.from_dict(self.SAMPLE)
        result = job.to_dict()
        for key in ["id", "status", "type", "backend", "shots"]:
            assert result[key] == self.SAMPLE[key]


class TestJobCreationResponse:
    SAMPLE = {
        "id": "617a1f8b-59d4-435d-aa33-695433d7155e",
        "status": "submitted",
        "session_id": None,
    }

    def test_from_dict(self):
        resp = JobCreationResponse.from_dict(self.SAMPLE)
        assert resp.id == "617a1f8b-59d4-435d-aa33-695433d7155e"
        assert resp.status == "submitted"

    def test_round_trip(self):
        resp = JobCreationResponse.from_dict(self.SAMPLE)
        result = resp.to_dict()
        assert result["id"] == self.SAMPLE["id"]
        assert result["status"] == self.SAMPLE["status"]


class TestWhoamiModel:
    SAMPLE = {
        "key_id": "e060759f-4348-4767-a645-8c0301265791",
        "key_name": "My First Key",
    }

    def test_from_dict(self):
        whoami = Whoami.from_dict(self.SAMPLE)
        assert whoami.key_id == UUID("e060759f-4348-4767-a645-8c0301265791")
        assert whoami.key_name == "My First Key"

    def test_round_trip(self):
        whoami = Whoami.from_dict(self.SAMPLE)
        assert whoami.to_dict() == self.SAMPLE


class TestSessionModel:
    SAMPLE = {
        "id": "abc123",
        "created_at": "2025-06-16T00:00:00Z",
        "organization_id": "org-123",
        "backend": "qpu.aria-1",
        "project_id": "proj-123",
        "creator_id": "user-123",
        "ended_at": None,
        "ender_id": None,
        "active": True,
        "status": "started",
        "started_at": "2025-06-16T00:00:00Z",
    }

    def test_from_dict(self):
        session = Session.from_dict(self.SAMPLE)
        assert session.id == "abc123"
        assert session.active is True
        assert session.status == "started"

    def test_round_trip(self):
        session = Session.from_dict(self.SAMPLE)
        result = session.to_dict()
        for key in ["id", "active", "status", "organization_id"]:
            assert result[key] == self.SAMPLE[key]
