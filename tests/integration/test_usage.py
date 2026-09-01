"""Integration tests for the usage endpoint."""

import datetime
import os

import pytest

from ionq_core.api.usage import get_usages
from ionq_core.exceptions import PermissionDeniedError

pytestmark = pytest.mark.integration


@pytest.fixture
def org_id():
    """Org id for org-scoped tests; skips the test when IONQ_ORG_ID is unset."""
    value = os.getenv("IONQ_ORG_ID")
    if not value:
        pytest.skip("org usage: set IONQ_ORG_ID (needs an org-admin-scoped key)")
    return value


def test_get_usages(client, org_id):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=30)
    try:
        result = get_usages.sync(
            org_id,
            client=client,
            start_date=start,
            end_date=today,
            group_by="project",
            modality="monthly",
        )
        assert result is not None
    except PermissionDeniedError:
        pytest.skip("API key lacks usage scope")
