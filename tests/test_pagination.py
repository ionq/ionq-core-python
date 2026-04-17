import pytest

from ionq_core import IonQError, aiter_jobs, aiter_session_jobs, iter_jobs, iter_session_jobs


def _jobs_page(job_ids, next_cursor=None):
    return {
        "jobs": [
            {
                "id": jid,
                "status": "completed",
                "type": "ionq.circuit.v1",
                "backend": "simulator",
                "dry_run": False,
                "submitter_id": "user-1",
                "project_id": None,
                "parent_job_id": None,
                "session_id": None,
                "metadata": None,
                "name": None,
                "submitted_at": None,
                "started_at": None,
                "completed_at": None,
                "predicted_wait_time_ms": None,
                "predicted_execution_duration_ms": None,
                "execution_duration_ms": None,
                "failure": None,
                "output": None,
                "settings": None,
                "stats": None,
                "results": None,
            }
            for jid in job_ids
        ],
        "next": next_cursor,
    }


class TestIterJobsNoneResponse:
    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    def test_sync_none_response(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch jobs"):
            list(iter_jobs(auth_client))

    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    async def test_async_none_response(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch jobs"):
            async for _ in aiter_jobs(auth_client):
                pass

    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    def test_sync_session_none_response(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch jobs"):
            list(iter_session_jobs(auth_client, "sess-1"))

    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    async def test_async_session_none_response(self, httpx_mock, auth_client):
        httpx_mock.add_response(status_code=500)
        auth_client.raise_on_unexpected_status = False
        with pytest.raises(IonQError, match="Failed to fetch jobs"):
            async for _ in aiter_session_jobs(auth_client, "sess-1"):
                pass


class TestIterJobs:
    def test_single_page(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1", "j2"]))
        jobs = list(iter_jobs(auth_client))
        assert [j.id for j in jobs] == ["j1", "j2"]

    def test_multiple_pages(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1"], next_cursor="cursor1"))
        httpx_mock.add_response(json=_jobs_page(["j2", "j3"]))
        jobs = list(iter_jobs(auth_client))
        assert [j.id for j in jobs] == ["j1", "j2", "j3"]

    def test_empty_page(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page([]))
        jobs = list(iter_jobs(auth_client))
        assert jobs == []


class TestAiterJobs:
    async def test_single_page(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1", "j2"]))
        jobs = [j async for j in aiter_jobs(auth_client)]
        assert [j.id for j in jobs] == ["j1", "j2"]

    async def test_multiple_pages(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1"], next_cursor="cursor1"))
        httpx_mock.add_response(json=_jobs_page(["j2"]))
        jobs = [j async for j in aiter_jobs(auth_client)]
        assert [j.id for j in jobs] == ["j1", "j2"]


class TestIterSessionJobs:
    def test_single_page(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1", "j2"]))
        jobs = list(iter_session_jobs(auth_client, "sess-1"))
        assert [j.id for j in jobs] == ["j1", "j2"]

    def test_multiple_pages(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1"], next_cursor="cursor1"))
        httpx_mock.add_response(json=_jobs_page(["j2"]))
        jobs = list(iter_session_jobs(auth_client, "sess-1"))
        assert [j.id for j in jobs] == ["j1", "j2"]


class TestAiterSessionJobs:
    async def test_single_page(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1"]))
        jobs = [j async for j in aiter_session_jobs(auth_client, "sess-1")]
        assert [j.id for j in jobs] == ["j1"]

    async def test_multiple_pages(self, httpx_mock, auth_client):
        httpx_mock.add_response(json=_jobs_page(["j1"], next_cursor="cursor1"))
        httpx_mock.add_response(json=_jobs_page(["j2"]))
        jobs = [j async for j in aiter_session_jobs(auth_client, "sess-1")]
        assert [j.id for j in jobs] == ["j1", "j2"]
