import pytest

from ionq_core import AuthenticatedClient, Client


def make_job_json(job_id, status="completed", **overrides):
    """Minimal valid job dict usable as both BaseJob and GetJobResponse."""
    return {
        "id": job_id,
        "status": status,
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "dry_run": False,
        "submitter_id": "user-1",
        "project_id": None,
        "parent_job_id": None,
        "session_id": None,
        "metadata": None,
        "name": None,
        "submitted_at": None,
        "started_at": None,
        "completed_at": None,
        "predicted_wait_time_ms": None,
        "predicted_execution_duration_ms": None,
        "execution_duration_ms": None,
        "failure": None,
        "output": {},
        "child_job_ids": None,
        "settings": {},
        "stats": {},
        "results": None,
        **overrides,
    }


@pytest.fixture
def client() -> Client:
    return Client(base_url="https://test.invalid/v0.4")


@pytest.fixture
def auth_client() -> AuthenticatedClient:
    return AuthenticatedClient(
        base_url="https://test.invalid/v0.4",
        token="test-api-key",
        prefix="apiKey",
        auth_header_name="Authorization",
    )
