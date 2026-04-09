from ionq_core import aiter_jobs, iter_jobs


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
            }
            for jid in job_ids
        ],
        "next": next_cursor,
    }


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
