"""Integration tests for characterization endpoints."""

import pytest

from ionq_core.api.characterizations import get_characterization, get_characterizations_for_backend

pytestmark = pytest.mark.integration

BACKEND = "qpu.forte-1"


@pytest.fixture
def latest_characterization(client):
    resp = get_characterizations_for_backend.sync(BACKEND, client=client, limit=1)
    assert resp is not None and resp.characterizations
    return resp.characterizations[0]


def test_list_characterizations(latest_characterization):
    assert latest_characterization.id
    assert latest_characterization.backend == BACKEND
    assert latest_characterization.date


def test_get_characterization_by_id(client, latest_characterization):
    char = get_characterization.sync(BACKEND, latest_characterization.id, client=client)
    assert char is not None
    assert char.id == latest_characterization.id
    assert char.qubits > 0
