"""Pact HTTP contract: ionq-core-python -> cloud-job-manager-http (GET /v0.4/jobs/{id}).
"""

from pathlib import Path

from pact import Pact, match

from ionq_core.api.default import get_job
from ionq_core.client import AuthenticatedClient
from ionq_core.models import SingleCircuitJob

PACT_DIR = Path(__file__).resolve().parents[3] / "pacts"

ISO_TIMESTAMP = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"

JOB_ID = "0198097d-3888-72ad-a9dd-9ace842cf181"

GET_RESPONSE_BODY = {
    "id": JOB_ID,
    "status": "completed",
    "type": "ionq.circuit.v1",
    "backend": match.string("simulator"),
    "dry_run": match.boolean(False),
    "submitter_id": match.string("66841feb7addb210ae6214c2"),
    "project_id": match.uuid("31a4dc21-9b52-4a51-89db-c62f1f77f356"),
    "parent_job_id": None,
    "session_id": None,
    "metadata": None,
    "name": match.string("pact test job"),
    "submitted_at": match.regex("2026-09-09T12:00:00.000Z", regex=ISO_TIMESTAMP),
    "started_at": None,
    "completed_at": None,
    "predicted_wait_time_ms": None,
    "predicted_execution_duration_ms": None,
    "execution_duration_ms": match.integer(0),
    "failure": None,
    "output": match.like({}),
    "settings": match.like({}),
    "stats": match.like({}),
    "results": {
        "ionq.result.probabilities.json.v1": match.like(
            {
                "id": match.string("probabilities"),
                "format": match.string("ionq.result.probabilities.json.v1"),
                "media_type": match.string("application/json"),
            }
        )
    },
    "child_job_ids": None,
}


def _client(mock_url: str) -> AuthenticatedClient:
    return AuthenticatedClient(
        base_url=f"{mock_url}/v0.4",
        token="pact-test-key",
        prefix="apiKey",
        auth_header_name="Authorization",
    )


def test_jobs_get_job_api_contract() -> None:
    pact = Pact("ionq-core-python", "cloud-job-manager-http").with_specification("V3")
    (
        pact.upon_receiving("a request to get a completed job")
        .given("a completed circuit job with results exists", id=JOB_ID)
        .with_request("GET", f"/v0.4/jobs/{JOB_ID}")
        .will_respond_with(200)
        .with_body(GET_RESPONSE_BODY, content_type="application/json")
    )
    with pact.serve() as srv, _client(srv.url) as client:
        job = get_job.sync(uuid=JOB_ID, client=client)
        assert isinstance(job, SingleCircuitJob)
        assert job.id == JOB_ID
        assert job.status == "completed"
        assert job.results is not None

    PACT_DIR.mkdir(exist_ok=True)
    pact.write_file(PACT_DIR, overwrite=False)
