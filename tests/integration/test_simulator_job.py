"""Submit a circuit to the simulator, poll to completion, verify results."""

import pytest

from ionq_core import wait_for_job
from ionq_core.api.default import create_job, get_job
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

pytestmark = pytest.mark.integration

BELL_CIRCUIT = {
    "type": "ionq.circuit.v1",
    "backend": "simulator",
    "shots": 100,
    "input": {
        "gateset": "qis",
        "circuit": [
            {"gate": "h", "targets": [0]},
            {"gate": "cnot", "targets": [0], "controls": [1]},
        ],
    },
}


def test_submit_and_poll(client, track_job):
    body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
    response = create_job.sync_detailed(client=client, body=body)
    assert response.status_code.value == 201
    job = response.parsed
    assert job is not None
    track_job(job.id)

    completed = wait_for_job(client, job.id, timeout=120)
    assert completed.status == "completed"


def test_get_job(client, track_job):
    body = CircuitJobCreationPayload.from_dict(BELL_CIRCUIT)
    response = create_job.sync_detailed(client=client, body=body)
    assert response.parsed is not None
    job_id = track_job(response.parsed.id)

    fetched = get_job.sync(uuid=job_id, client=client)
    assert fetched is not None
    assert fetched.id == job_id
