"""Integration tests for characterization endpoints."""

import pytest

from ionq_core.api.characterizations import get_characterization, get_characterizations_for_backend

pytestmark = pytest.mark.integration


class TestListCharacterizations:
    def test_returns_characterizations(self, client):
        resp = get_characterizations_for_backend.sync("qpu.forte-1", client=client, limit=1)
        assert resp is not None
        assert len(resp.characterizations) > 0

    def test_characterization_fields(self, client):
        resp = get_characterizations_for_backend.sync("qpu.forte-1", client=client, limit=1)
        char = resp.characterizations[0]
        assert char.id
        assert char.backend == "qpu.forte-1"
        assert char.date


class TestGetCharacterization:
    def test_get_by_id(self, client):
        resp = get_characterizations_for_backend.sync("qpu.forte-1", client=client, limit=1)
        char_id = resp.characterizations[0].id

        char = get_characterization.sync("qpu.forte-1", char_id, client=client)
        assert char is not None
        assert char.id == char_id
        assert char.qubits > 0
