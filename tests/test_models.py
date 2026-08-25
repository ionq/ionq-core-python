from uuid import UUID

from ionq_core.models.backend import Backend
from ionq_core.models.base_job import BaseJob
from ionq_core.models.job_creation_response import JobCreationResponse
from ionq_core.models.qctrl_qaoa_job_creation_payload import QctrlQaoaJobCreationPayload
from ionq_core.models.qctrl_qaoa_job_creation_payload_external_settings import (
    QctrlQaoaJobCreationPayloadExternalSettings,
)
from ionq_core.models.session import Session
from ionq_core.models.whoami import Whoami

BACKEND_SAMPLE = {
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

JOB_SAMPLE = {
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

JOB_CREATION_SAMPLE = {
    "id": "617a1f8b-59d4-435d-aa33-695433d7155e",
    "status": "submitted",
    "session_id": None,
}

WHOAMI_SAMPLE = {
    "key_id": "e060759f-4348-4767-a645-8c0301265791",
    "key_name": "My First Key",
}

SESSION_SAMPLE = {
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


class TestBackendModel:
    def test_from_dict(self):
        b = Backend.from_dict(BACKEND_SAMPLE)
        assert b.backend == "qpu.aria-1"
        assert b.status == "available"
        assert b.degraded is False
        assert b.qubits == 25
        assert b.average_queue_time == 1181215
        assert b.characterization_id == "617a1f8b-59d4-435d-aa33-695433d7155e"

    def test_round_trip(self):
        assert Backend.from_dict(BACKEND_SAMPLE).to_dict() == BACKEND_SAMPLE


class TestJobModel:
    def test_from_dict(self):
        j = BaseJob.from_dict(JOB_SAMPLE)
        assert j.id == "e1a09d90-b2ba-4ea5-9fd7-4bfc14eac524"
        assert j.status == "failed"
        assert j.backend == "simulator"
        assert j.shots == 1000

    def test_round_trip(self):
        result = BaseJob.from_dict(JOB_SAMPLE).to_dict()
        for key in ["id", "status", "type", "backend", "shots"]:
            assert result[key] == JOB_SAMPLE[key]


class TestJobCreationResponse:
    def test_from_dict(self):
        r = JobCreationResponse.from_dict(JOB_CREATION_SAMPLE)
        assert r.id == "617a1f8b-59d4-435d-aa33-695433d7155e"
        assert r.status == "submitted"

    def test_round_trip(self):
        result = JobCreationResponse.from_dict(JOB_CREATION_SAMPLE).to_dict()
        assert result["id"] == JOB_CREATION_SAMPLE["id"]
        assert result["status"] == JOB_CREATION_SAMPLE["status"]


class TestWhoamiModel:
    def test_from_dict(self):
        w = Whoami.from_dict(WHOAMI_SAMPLE)
        assert w.key_id == UUID("e060759f-4348-4767-a645-8c0301265791")
        assert w.key_name == "My First Key"

    def test_round_trip(self):
        assert Whoami.from_dict(WHOAMI_SAMPLE).to_dict() == WHOAMI_SAMPLE


class TestSessionModel:
    def test_from_dict(self):
        s = Session.from_dict(SESSION_SAMPLE)
        assert s.id == "abc123"
        assert s.active is True
        assert s.status == "started"

    def test_round_trip(self):
        result = Session.from_dict(SESSION_SAMPLE).to_dict()
        for key in ["id", "active", "status", "organization_id"]:
            assert result[key] == SESSION_SAMPLE[key]


class TestQctrlCredentialMasking:
    """api_credentials is a Q-CTRL API key. repr()/str() must never leak it (CWE-532); to_dict() must keep it."""

    SECRET = "qctrl-secret-key-123"

    def _payload(self):
        return QctrlQaoaJobCreationPayload.from_dict(
            {
                "backend": "simulator",
                "type": "qctrl.qaoa.v1",
                "input": {"problem_type": "maxcut", "problem": {}},
                "external_settings": {"api_credentials": self.SECRET},
            }
        )

    def test_external_settings_repr_masked(self):
        settings = QctrlQaoaJobCreationPayloadExternalSettings(api_credentials=self.SECRET)
        assert self.SECRET not in repr(settings)
        assert self.SECRET not in str(settings)

    def test_containing_payload_repr_masked(self):
        payload = self._payload()
        assert self.SECRET not in repr(payload)
        assert self.SECRET not in str(payload)

    def test_credential_round_trips_to_wire_format(self):
        payload = self._payload()
        assert payload.external_settings.api_credentials == self.SECRET
        assert payload.to_dict()["external_settings"]["api_credentials"] == self.SECRET
