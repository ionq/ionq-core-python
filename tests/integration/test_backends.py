"""Integration tests for backend endpoints."""

import pytest

from ionq_core import Client
from ionq_core.api.backends import get_backend, get_backends

pytestmark = pytest.mark.integration

BASE_URL = "https://api.ionq.co/v0.4"


class TestListBackends:
    @pytest.fixture(autouse=True)
    def _fetch(self):
        self.backends = get_backends.sync(client=Client(base_url=BASE_URL))

    def test_returns_backends(self):
        assert len(self.backends) > 0

    def test_has_qpu(self):
        assert any("qpu" in b.backend for b in self.backends)

    def test_fields(self):
        for b in self.backends:
            assert b.backend
            assert b.status
            assert b.qubits > 0
            assert b.last_updated


class TestGetBackend:
    def test_get_qpu(self, client):
        backend = get_backend.sync("qpu.forte-1", client=client)
        assert backend is not None
        assert backend.backend == "qpu.forte-1"
        assert backend.qubits > 0
