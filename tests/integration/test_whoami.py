"""Integration tests for the whoami endpoint."""

import pytest

from ionq_core.api.whoami import get_whoami

pytestmark = pytest.mark.integration


def test_whoami(client):
    result = get_whoami.sync(client=client)
    assert result is not None
    assert result.key_name


def test_whoami_detailed(client):
    resp = get_whoami.sync_detailed(client=client)
    assert resp.status_code.value == 200
    assert resp.parsed is not None
    assert resp.parsed.key_id
