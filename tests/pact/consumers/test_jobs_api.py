"""Pact HTTP contract: ionq-core-python -> cloud-job-manager-http.

Consumes POST /v0.4/jobs (create -> 201) and GET /v0.4/jobs/{id} (fetch a
completed job -> 200). Generated openapi-python-client: from_dict parse IS
consumption, so the GET asserts every required key. Use the bare
AuthenticatedClient (not the IonQClient factory) — its UA / non-HTTPS warnings
would trip this repo's filterwarnings=error.
"""

from pathlib import Path

from pact import Pact, match

from ionq_core.api.default import create_job, get_job
from ionq_core.client import AuthenticatedClient
from ionq_core.models import (
    CircuitJobCreationPayload,
    JobCreationResponse,
    SingleCircuitJob,
)

PACT_DIR = Path(__file__).resolve().parents[3] / "pacts"

ISO_TIMESTAMP = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"

# Pinned with cloud-job-manager's provider state handler ('a completed circuit
# job with results exists' seeds this exact id from the state parameters).
JOB_ID = "0198097d-3888-72ad-a9dd-9ace842cf181"

# The real request model drives the pact request body (never hand-written, so
# it can't drift from what the SDK serializes). Enriched with the optional
# fields the SDK really sends: name, settings.error_mitigation and noise.
# attrs' to_dict() drops UNSET fields, but shots defaults to 100 (not UNSET)
# and is therefore always on the wire.
CREATE_PAYLOAD = CircuitJobCreationPayload.from_dict(
    {
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "name": "pact test job",
        "shots": 100,
        "input": {
            "gateset": "qis",
            "qubits": 2,
            "circuit": [
                {"gate": "h", "target": 0},
                {"gate": "cnot", "target": 0, "control": 1},
            ],
        },
        "settings": {"error_mitigation": {"debiasing": False}},
        "noise": {"model": "ideal"},
    }
)

CREATE_RESPONSE_BODY = {
    "id": match.uuid("0198097d-3888-72ad-a9dd-9ace842cf182"),
    "status": "submitted",
    # Required-nullable: the key must be on the wire (null for sessionless).
    "session_id": None,
}

# Every SingleCircuitJob required key, with the values the provider state's
# seed produces; required-nullable keys are asserted as null. results pins the
# format-keyed v1 descriptor the provider synthesizes (its legacy {url}
# entries ride along as unasserted extras).
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
    # Null for completed jobs (the wait is over); the SDK only needs the key.
    "predicted_wait_time_ms": None,
    "predicted_execution_duration_ms": None,
    # The provider computes this and sends 0 when no execution times exist.
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


def test_jobs_api_contract() -> None:
    pact = Pact("ionq-core-python", "cloud-job-manager-http").with_specification("V3")

    (
        pact.upon_receiving("a request to create a circuit job")
        .given("a valid project and org region exist")
        .with_request("POST", "/v0.4/jobs")
        .with_body(CREATE_PAYLOAD.to_dict(), content_type="application/json")
        .will_respond_with(201)
        .with_body(CREATE_RESPONSE_BODY, content_type="application/json")
    )
    (
        pact.upon_receiving("a request to get a completed job")
        .given("a completed circuit job with results exists", id=JOB_ID)
        .with_request("GET", f"/v0.4/jobs/{JOB_ID}")
        .will_respond_with(200)
        .with_body(GET_RESPONSE_BODY, content_type="application/json")
    )

    with (
        pact.serve() as srv,
        AuthenticatedClient(
            base_url=f"{srv.url}/v0.4",
            token="pact-test-key",
            prefix="apiKey",
            auth_header_name="Authorization",
        ) as client,
    ):
        created = create_job.sync(client=client, body=CREATE_PAYLOAD)
        assert isinstance(created, JobCreationResponse)
        assert created.status == "submitted"
        assert created.session_id is None

        job = get_job.sync(uuid=JOB_ID, client=client)
        assert isinstance(job, SingleCircuitJob)
        assert job.id == JOB_ID
        assert job.status == "completed"
        assert job.results is not None

    PACT_DIR.mkdir(exist_ok=True)
    pact.write_file(PACT_DIR, overwrite=True)
