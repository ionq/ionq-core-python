import json

import httpx
import pytest

from ionq_core._exceptions import IonQError
from ionq_core._session import SessionManager

_BASE = "https://test.invalid/v0.4"


def _session_json(session_id="sess-1", status="created", active=True):
    return {
        "id": session_id,
        "created_at": "2025-01-01T00:00:00Z",
        "organization_id": "org-1",
        "backend": "qpu.aria-1",
        "project_id": None,
        "creator_id": None,
        "ended_at": None,
        "ender_id": None,
        "active": active,
        "status": status,
        "started_at": None,
    }


_ENDED = {"active": False, "status": "ended"}


class TestContextManager:
    def test_creates_and_ends_session(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST", url=f"{_BASE}/sessions")
        httpx_mock.add_response(json=_session_json(**_ENDED), method="POST", url=f"{_BASE}/sessions/sess-1/end")

        with SessionManager(auth_client, "qpu.aria-1") as mgr:
            assert mgr.session_id == "sess-1"

        reqs = httpx_mock.get_requests()
        assert reqs[0].method == "POST" and reqs[0].url.path == "/v0.4/sessions"
        assert "/sessions/sess-1/end" in str(reqs[1].url)

    def test_end_called_on_exception(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST", url=f"{_BASE}/sessions")
        httpx_mock.add_response(json=_session_json(active=False), method="POST", url=f"{_BASE}/sessions/sess-1/end")

        with pytest.raises(ValueError, match="boom"), SessionManager(auth_client, "qpu.aria-1"):
            raise ValueError("boom")

        assert "/sessions/sess-1/end" in str(httpx_mock.get_requests()[1].url)


class TestSettings:
    def test_settings_passed_in_body(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_response(json=_session_json(active=False), method="POST")

        with SessionManager(auth_client, "qpu.aria-1", max_jobs=10, max_time=60, max_cost=5.0):
            pass

        data = json.loads(httpx_mock.get_requests()[0].content)
        assert data["backend"] == "qpu.aria-1"
        assert data["settings"]["job_count_limit"] == 10
        assert data["settings"]["duration_limit_min"] == 60
        assert data["settings"]["cost_limit"] == {"unit": "usd", "value": 5.0}


class TestFromId:
    def test_reconnects_without_creating(self, httpx_mock, auth_client):
        mgr = SessionManager.from_id(auth_client, "sess-existing")
        assert mgr.session_id == "sess-existing"
        assert httpx_mock.get_requests() == []

    def test_close_from_id(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_session_json(session_id="sess-existing", active=False), method="POST")
        mgr = SessionManager.from_id(auth_client, "sess-existing")
        mgr.close()
        assert "/sessions/sess-existing/end" in str(httpx_mock.get_requests()[0].url)


class TestStatus:
    def test_queries_session(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_response(json=_session_json(status="started"), method="GET")
        httpx_mock.add_response(json=_session_json(active=False), method="POST")

        with SessionManager(auth_client, "qpu.aria-1") as mgr:
            assert mgr.status() == "started"


class TestOpenClose:
    def test_open_close_outside_context(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_response(json=_session_json(active=False), method="POST")

        mgr = SessionManager(auth_client, "qpu.aria-1")
        mgr.open()
        assert mgr.session_id == "sess-1"
        mgr.close()

        reqs = httpx_mock.get_requests()
        assert reqs[0].url.path == "/v0.4/sessions"
        assert "/sessions/sess-1/end" in str(reqs[1].url)

    def test_open_when_already_open_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        mgr = SessionManager(auth_client, "qpu.aria-1")
        mgr.open()
        with pytest.raises(IonQError, match="already open"):
            mgr.open()

    def test_open_returns_none_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500, method="POST")
        auth_client.raise_on_unexpected_status = False
        mgr = SessionManager(auth_client, "qpu.aria-1")
        with pytest.raises(IonQError, match="Failed to create session"):
            mgr.open()

    def test_close_suppresses_exception(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_exception(httpx.ConnectError("network down"), method="POST", url=f"{_BASE}/sessions/sess-1/end")
        mgr = SessionManager(auth_client, "qpu.aria-1")
        mgr.open()
        mgr.close()

    def test_close_without_session_is_noop(self, httpx_mock, auth_client):
        mgr = SessionManager(auth_client, "qpu.aria-1")
        mgr.close()
        assert httpx_mock.get_requests() == []


class TestAsyncContextManager:
    async def test_creates_and_ends_session(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST", url=f"{_BASE}/sessions")
        httpx_mock.add_response(json=_session_json(**_ENDED), method="POST", url=f"{_BASE}/sessions/sess-1/end")

        async with SessionManager(auth_client, "qpu.aria-1") as mgr:
            assert mgr.session_id == "sess-1"

        reqs = httpx_mock.get_requests()
        assert reqs[0].method == "POST" and reqs[0].url.path == "/v0.4/sessions"
        assert "/sessions/sess-1/end" in str(reqs[1].url)

    async def test_end_called_on_exception(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST", url=f"{_BASE}/sessions")
        httpx_mock.add_response(json=_session_json(active=False), method="POST", url=f"{_BASE}/sessions/sess-1/end")

        with pytest.raises(ValueError, match="boom"):
            async with SessionManager(auth_client, "qpu.aria-1"):
                raise ValueError("boom")

        assert "/sessions/sess-1/end" in str(httpx_mock.get_requests()[1].url)


class TestAsyncOpenClose:
    async def test_async_open_close(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_response(json=_session_json(active=False), method="POST")

        mgr = SessionManager(auth_client, "qpu.aria-1")
        await mgr.async_open()
        assert mgr.session_id == "sess-1"
        await mgr.async_close()

    async def test_async_open_when_already_open_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        mgr = SessionManager(auth_client, "qpu.aria-1")
        await mgr.async_open()
        with pytest.raises(IonQError, match="already open"):
            await mgr.async_open()

    async def test_async_open_returns_none_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500, method="POST")
        auth_client.raise_on_unexpected_status = False
        mgr = SessionManager(auth_client, "qpu.aria-1")
        with pytest.raises(IonQError, match="Failed to create session"):
            await mgr.async_open()

    async def test_async_close_suppresses_exception(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_exception(httpx.ConnectError("network down"), method="POST", url=f"{_BASE}/sessions/sess-1/end")
        mgr = SessionManager(auth_client, "qpu.aria-1")
        await mgr.async_open()
        await mgr.async_close()

    async def test_async_close_without_session_is_noop(self, httpx_mock, auth_client):
        mgr = SessionManager(auth_client, "qpu.aria-1")
        await mgr.async_close()
        assert httpx_mock.get_requests() == []


class TestAsyncStatus:
    async def test_async_queries_session(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=201, json=_session_json(), method="POST")
        httpx_mock.add_response(json=_session_json(status="started"), method="GET")
        httpx_mock.add_response(json=_session_json(active=False), method="POST")

        async with SessionManager(auth_client, "qpu.aria-1") as mgr:
            assert await mgr.async_status() == "started"

    async def test_async_status_without_session_raises(self, auth_client):
        mgr = SessionManager(auth_client, "qpu.aria-1")
        with pytest.raises(IonQError, match="No session ID"):
            await mgr.async_status()

    async def test_async_status_returns_none_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500, method="GET")
        auth_client.raise_on_unexpected_status = False
        mgr = SessionManager.from_id(auth_client, "sess-1")
        with pytest.raises(IonQError, match="Failed to fetch session"):
            await mgr.async_status()


class TestStatusErrors:
    def test_status_without_session_raises(self, auth_client):
        mgr = SessionManager(auth_client, "qpu.aria-1")
        with pytest.raises(IonQError, match="No session ID"):
            mgr.status()

    def test_status_returns_none_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500, method="GET")
        auth_client.raise_on_unexpected_status = False
        mgr = SessionManager.from_id(auth_client, "sess-1")
        with pytest.raises(IonQError, match="Failed to fetch session"):
            mgr.status()
