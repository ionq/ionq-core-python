"""Smoke test: verify the API key is valid."""

import pytest

from ionq_core.api.whoami import get_whoami

pytestmark = pytest.mark.integration


def test_whoami(client):
    result = get_whoami.sync(client=client)
    assert result is not None
    assert result.key_name
