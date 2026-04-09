"""Verify backend listing works against the real API."""

import pytest

from ionq_core import Client
from ionq_core.api.backends import get_backends

pytestmark = pytest.mark.integration


def test_list_backends():
    """Backends endpoint is unauthenticated - use a plain Client."""
    unauthenticated = Client(base_url="https://api.ionq.co/v0.4")
    backends = get_backends.sync(client=unauthenticated)
    assert backends is not None
    assert len(backends) > 0
    names = [b.backend for b in backends]
    assert any("qpu" in n for n in names), f"Expected at least one QPU backend in {names}"
