"""Integration tests for session endpoints."""

import contextlib

import pytest

from ionq_core import SessionManager
from ionq_core._exceptions import NotFoundError
from ionq_core.api.default import get_session_jobs, get_sessions

pytestmark = pytest.mark.integration


def test_list_sessions(client):
    try:
        result = get_sessions.sync(client=client)
        assert result is not None
    except NotFoundError:
        pytest.skip("Sessions endpoint not available for this account")


class TestSessionManager:
    def test_create_and_end_session(self, client):
        mgr = SessionManager(client, "simulator")
        try:
            mgr.open()
        except NotFoundError:
            pytest.skip("Sessions not available for this account")

        try:
            assert mgr.session_id is not None

            session = mgr.status()
            assert session is not None
            assert session.backend == "simulator"

            jobs = get_session_jobs.sync(mgr.session_id, client=client)
            assert jobs is not None
        finally:
            with contextlib.suppress(Exception):
                mgr.close()

    def test_context_manager(self, client):
        mgr = SessionManager(client, "simulator")
        try:
            mgr.open()
        except NotFoundError:
            pytest.skip("Sessions not available for this account")
        try:
            assert mgr.session_id is not None
            status = mgr.status()
            assert status is not None
        finally:
            with contextlib.suppress(Exception):
                mgr.close()
