"""Pact HTTP contract: ionq-core-python -> cloud-job-manager-http (POST /v0.4/jobs).
"""

from pathlib import Path

from pact import Pact, match

from ionq_core.api.default import create_job
from ionq_core.client import AuthenticatedClient
from ionq_core.models import CircuitJobCreationPayload, JobCreationResponse

PACT_DIR = Path(__file__).resolve().parents[3] / "pacts"

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

# Only the fields the SDK reads off the create response.
CREATE_RESPONSE_BODY = {
    "id": match.uuid("0198097d-3888-72ad-a9dd-9ace842cf182"),
    "status": "submitted",
    "session_id": None,
}


def _client(mock_url: str) -> AuthenticatedClient:
    return AuthenticatedClient(
        base_url=f"{mock_url}/v0.4",
        token="pact-test-key",
        prefix="apiKey",
        auth_header_name="Authorization",
    )


def test_jobs_create_circuit_api_contract() -> None:
    pact = Pact("ionq-core-python", "cloud-job-manager-http").with_specification("V3")
    (
        pact.upon_receiving("a request to create a circuit job")
        .given("a valid project and org region exist")
        .with_request("POST", "/v0.4/jobs")
        .with_body(CREATE_PAYLOAD.to_dict(), content_type="application/json")
        .will_respond_with(201)
        .with_body(CREATE_RESPONSE_BODY, content_type="application/json")
    )
    with pact.serve() as srv, _client(srv.url) as client:
        created = create_job.sync(client=client, body=CREATE_PAYLOAD)
        assert isinstance(created, JobCreationResponse)
        assert created.status == "submitted"
        assert created.session_id is None

    PACT_DIR.mkdir(exist_ok=True)
    pact.write_file(PACT_DIR, overwrite=False)
