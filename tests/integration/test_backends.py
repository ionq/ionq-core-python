"""Integration tests for backend endpoints."""

import warnings

import pytest

from ionq_core import Client
from ionq_core.api.backends import get_backend, get_backends

pytestmark = pytest.mark.integration

BASE_URL = "https://api.ionq.co/v0.4"


def _unauthenticated():
    """Unauthenticated client (no managed transport, may leak sockets)."""
    return Client(base_url=BASE_URL)


class TestListBackends:
    def test_returns_backends(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            backends = get_backends.sync(client=_unauthenticated())
        assert backends is not None
        assert len(backends) > 0

    def test_has_qpu(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            backends = get_backends.sync(client=_unauthenticated())
        names = [b.backend for b in backends]
        assert any("qpu" in n for n in names)

    def test_backend_fields(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            backends = get_backends.sync(client=_unauthenticated())
        for b in backends:
            assert b.backend
            assert b.status
            assert b.qubits > 0
            assert b.average_queue_time is not None
            assert b.last_updated


class TestGetBackend:
    def test_get_qpu(self, client):
        backend = get_backend.sync("qpu.forte-1", client=client)
        assert backend is not None
        assert backend.backend == "qpu.forte-1"
        assert backend.qubits > 0
