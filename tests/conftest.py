from urllib.parse import urlparse

import httpx
import pytest

from ionq_core import AuthenticatedClient, Client
from ionq_core.ionq_client import DEFAULT_BASE_URL

BASE_URL = "https://test.invalid" + urlparse(DEFAULT_BASE_URL).path


class FakeTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    """Returns (or raises) the queued items in order."""

    def __init__(self, *responses):
        self._responses = list(responses)
        self.call_count = 0

    def _next(self):
        self.call_count += 1
        item = self._responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def handle_request(self, request):
        return self._next()

    async def handle_async_request(self, request):
        return self._next()


def make_job_json(job_id, status="completed", **overrides):
    """Minimal valid job dict usable as both BaseJob and SingleCircuitJob."""
    return {
        "id": job_id,
        "status": status,
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
        "output": {},
        "child_job_ids": None,
        "settings": {},
        "stats": {},
        "results": None,
        **overrides,
    }


@pytest.fixture
def client() -> Client:
    return Client(base_url=BASE_URL)


@pytest.fixture
def auth_client() -> AuthenticatedClient:
    return AuthenticatedClient(
        base_url=BASE_URL,
        token="test-api-key",
        prefix="apiKey",
        auth_header_name="Authorization",
    )
