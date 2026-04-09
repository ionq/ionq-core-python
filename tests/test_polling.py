import pytest

from ionq_core._polling import JobFailedError, JobTimeoutError, async_wait_for_job, wait_for_job


def _job_response(job_id, status, failure=None):
    resp = {
        "id": job_id,
        "status": status,
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "dry_run": False,
        "submitter_id": "user-1",
    }
    if failure:
        resp["failure"] = failure
    return resp


class TestWaitForJob:
    def test_already_completed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_job_response("j1", "completed"))
        job = wait_for_job(auth_client, "j1", timeout=5)
        assert job.status == "completed"

    def test_polls_until_completed(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core._polling.time.sleep", lambda _: None)
        httpx_mock.add_response(json=_job_response("j1", "submitted"))
        httpx_mock.add_response(json=_job_response("j1", "ready"))
        httpx_mock.add_response(json=_job_response("j1", "completed"))
        job = wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=10)
        assert job.status == "completed"

    def test_raises_on_failure(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            json=_job_response("j1", "failed", failure={"code": "SimulationError", "message": "boom"})
        )
        with pytest.raises(JobFailedError, match="j1"):
            wait_for_job(auth_client, "j1", timeout=5)

    def test_no_raise_on_failure_when_disabled(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            json=_job_response("j1", "failed", failure={"code": "SimulationError", "message": "boom"})
        )
        job = wait_for_job(auth_client, "j1", timeout=5, raise_on_failure=False)
        assert job.status == "failed"

    def test_canceled_returns(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_job_response("j1", "canceled"))
        job = wait_for_job(auth_client, "j1", timeout=5)
        assert job.status == "canceled"

    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    def test_timeout_raises(self, httpx_mock, auth_client, monkeypatch):
        monkeypatch.setattr("ionq_core._polling.time.sleep", lambda _: None)
        for _ in range(50):
            httpx_mock.add_response(json=_job_response("j1", "submitted"))
        with pytest.raises(JobTimeoutError, match="j1"):
            wait_for_job(auth_client, "j1", poll_interval=0.01, timeout=0.0)


class TestAsyncWaitForJob:
    async def test_already_completed(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_job_response("j1", "completed"))
        job = await async_wait_for_job(auth_client, "j1", timeout=5)
        assert job.status == "completed"

    async def test_raises_on_failure(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            json=_job_response("j1", "failed", failure={"code": "SimulationError", "message": "boom"})
        )
        with pytest.raises(JobFailedError, match="j1"):
            await async_wait_for_job(auth_client, "j1", timeout=5)

    async def test_canceled_returns(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_job_response("j1", "canceled"))
        job = await async_wait_for_job(auth_client, "j1", timeout=5)
        assert job.status == "canceled"
