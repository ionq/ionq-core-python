"""Integration tests verifying async variants work against the real API."""

import pytest

from ionq_core import IonQClient, aiter_jobs
from ionq_core.api.default import get_jobs
from ionq_core.api.whoami import get_whoami

pytestmark = pytest.mark.integration


@pytest.fixture
def async_client(api_key, base_url):
    """Separate client instance - the session-scoped client may not have an async transport."""
    return IonQClient(api_key=api_key, base_url=base_url)


async def test_async_whoami(async_client):
    async with async_client as c:
        result = await get_whoami.asyncio(client=c)
        assert result is not None
        assert result.key_name


async def test_async_list_jobs(async_client):
    async with async_client as c:
        resp = await get_jobs.asyncio(client=c, limit=2)
        assert resp is not None
        assert len(resp.jobs) > 0


async def test_async_iter_jobs(async_client):
    async with async_client as c:
        jobs = []
        async for j in aiter_jobs(c, limit=1):
            jobs.append(j)
            if len(jobs) >= 2:
                break
        assert len(jobs) == 2
