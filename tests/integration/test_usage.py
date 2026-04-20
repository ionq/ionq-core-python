"""Integration tests for the usage endpoint."""

import datetime

import pytest

from ionq_core._exceptions import PermissionDeniedError
from ionq_core.api.usage import get_usages

pytestmark = pytest.mark.integration


def test_get_usages(client):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=30)
    try:
        result = get_usages.sync(
            "self",
            client=client,
            start_date=start,
            end_date=today,
            group_by="project",
            modality="monthly",
        )
        assert result is not None
    except PermissionDeniedError:
        pytest.skip("API key lacks usage scope")
