# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

import pytest

from examples import hamiltonian_energy_optimization as example


def test_hamiltonian_energy_payload_uses_typed_models():
    payload = example.build_hamiltonian_energy_payload([0.25], shots=200)

    assert payload.to_dict() == {
        "backend": "simulator",
        "type": "quantum-function",
        "input": {
            "data": {
                "type": "hamiltonian-energy",
                "data": {
                    "hamiltonian": [{"pauli_string": "Z", "coefficient": -1.0}],
                    "ansatz": {"data": example.ANSATZ_OPENQASM},
                    "penalty": 0.0,
                },
            },
            "params": [0.25],
        },
        "name": "ionq-core hamiltonian energy example",
        "shots": 200,
    }


def test_evaluate_energy_submits_payload_and_polls_job(auth_client):
    calls = []

    class CreatedJob:
        id = "job-123"

    class CompletedOutput:
        def to_dict(self):
            return {"energy": -0.75}

    class CompletedJob:
        output = CompletedOutput()

    def fake_create_job(*, client, body):
        calls.append(("create", client, body.to_dict()))
        return CreatedJob()

    def fake_wait_for_job(client, job_id, *, poll_interval, timeout):
        calls.append(("wait", client, job_id, poll_interval, timeout))
        return CompletedJob()

    energy = example.evaluate_energy(
        auth_client,
        [0.5],
        create_job_sync=fake_create_job,
        wait_for_job_fn=fake_wait_for_job,
        poll_interval=0.25,
        timeout=12.0,
    )

    assert energy == -0.75
    assert calls[0][0] == "create"
    assert calls[0][1] is auth_client
    assert calls[0][2]["input"]["params"] == [0.5]
    assert calls[1] == ("wait", auth_client, "job-123", 0.25, 12.0)


def test_coordinate_search_reports_and_lowers_energy():
    messages = []

    def bowl(params):
        return (params[0] - 0.25) ** 2

    result = example.coordinate_search(
        bowl,
        [1.25],
        step_size=0.5,
        min_step=0.125,
        max_iterations=4,
        log=messages.append,
    )

    assert result.energy == pytest.approx(0.0)
    assert result.parameters == pytest.approx([0.25])
    assert result.history[-1] == (2, [0.25], 0.0)
    assert any(message.startswith("iteration 2:") for message in messages)
