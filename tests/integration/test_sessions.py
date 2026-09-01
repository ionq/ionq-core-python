"""Integration tests for session endpoints."""

import pytest

from ionq_core import SessionManager
from ionq_core.api.default import get_session_jobs, get_sessions
from ionq_core.exceptions import NotFoundError

pytestmark = pytest.mark.integration


def test_list_sessions(client):
    try:
        result = get_sessions.sync(client=client)
        assert result is not None
    except NotFoundError:
        pytest.skip("Sessions endpoint not available for this account")


def test_session_lifecycle(client):
    try:
        with SessionManager(client, "simulator") as session:
            assert session.session_id is not None
            assert session.status() in ("created", "started", "ready")

            jobs = get_session_jobs.sync(session.session_id, client=client)
            assert jobs is not None
    except NotFoundError:
        pytest.skip("Sessions not available for this account")
