import asyncio

import pytest

from ionq_core.exceptions import IonQError
from ionq_core.polling import JobFailedError, JobTimeoutError, async_wait_for_job, wait_for_job
from tests.conftest import make_job_json

# Captured at import time so tests can call the real sleep after monkeypatching ionq_core.polling.asyncio.sleep.
_real_sleep = asyncio.sleep

_FAILURE = {"code": "SimulationError", "message": "boom"}


class TestWaitForJob:
    def test_already_completed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "completed"))
        assert wait_for_job(auth_client, "j1", timeout=5).status == "completed"

    def test_polls_until_completed(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core.polling.time.sleep", lambda _: None)
        for s in ("submitted", "ready", "completed"):
            httpx_mock.add_response(json=make_job_json("j1", s))
        assert wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=10).status == "completed"

    def test_raises_on_failure(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "failed", failure=_FAILURE))
        with pytest.raises(JobFailedError, match="j1"):
            wait_for_job(auth_client, "j1", timeout=5)

    def test_no_raise_on_failure_when_disabled(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "failed", failure=_FAILURE))
        assert wait_for_job(auth_client, "j1", timeout=5, raise_on_failure=False).status == "failed"

    def test_canceled_returns(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "canceled"))
        assert wait_for_job(auth_client, "j1", timeout=5).status == "canceled"

    def test_none_response_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch job"):
            wait_for_job(auth_client, "j1", timeout=5)

    def test_timeout_raises(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core.polling.time.sleep", lambda _: None)
        httpx_mock.add_response(json=make_job_json("j1", "submitted"), is_reusable=True)
        with pytest.raises(JobTimeoutError, match="j1"):
            wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=0.0)


class TestAsyncWaitForJob:
    async def test_already_completed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "completed"))
        assert (await async_wait_for_job(auth_client, "j1", timeout=5)).status == "completed"

    async def test_raises_on_failure(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=make_job_json("j1", "failed", failure=_FAILURE))
        with pytest.raises(JobFailedError, match="j1"):
            await async_wait_for_job(auth_client, "j1", timeout=5)

    async def test_none_response_raises(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch job"):
            await async_wait_for_job(auth_client, "j1", timeout=5)

    async def test_timeout_raises(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core.polling.asyncio.sleep", lambda _: _real_sleep(0))
        httpx_mock.add_response(json=make_job_json("j1", "submitted"), is_reusable=True)
        with pytest.raises(JobTimeoutError, match="j1"):
            await async_wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=0.0)

    async def test_polls_until_completed(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core.polling.asyncio.sleep", lambda _: _real_sleep(0))
        for s in ("submitted", "ready", "completed"):
            httpx_mock.add_response(json=make_job_json("j1", s))
        result = await async_wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=10)
        assert result.status == "completed"
