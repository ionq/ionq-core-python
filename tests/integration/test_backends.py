"""Integration tests for backend endpoints."""

import pytest

from ionq_core import Client
from ionq_core.api.backends import get_backend, get_backends

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def backends(base_url: str):
    # Backends listing is unauthenticated - no API key needed.
    return get_backends.sync(client=Client(base_url=base_url))


def test_list_returns_backends(backends):
    assert len(backends) > 0


def test_list_has_qpu(backends):
    assert any("qpu" in b.backend for b in backends)


def test_list_fields(backends):
    for b in backends:
        assert b.backend
        assert b.status
        assert b.qubits > 0
        assert b.last_updated


def test_get_backend_qpu(client):
    backend = get_backend.sync("qpu.forte-1", client=client)
    assert backend is not None
    assert backend.backend == "qpu.forte-1"
    assert backend.qubits > 0
