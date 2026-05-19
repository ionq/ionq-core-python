"""Fixtures for integration tests against the real IonQ API."""

import contextlib
import os

import pytest

from ionq_core import AuthenticatedClient, IonQClient
from ionq_core.api.default import delete_job


@pytest.fixture(scope="session")
def api_key() -> str:
    key = os.environ.get("IONQ_API_KEY")
    if not key:
        pytest.skip("IONQ_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def client(api_key: str) -> AuthenticatedClient:
    return IonQClient(api_key=api_key)


@pytest.fixture(scope="session")
def _tracked_jobs() -> list[str]:
    """Session-scoped list of job IDs to delete in `cleanup_jobs`."""
    return []


@pytest.fixture
def track_job(_tracked_jobs: list[str]):
    """Register a job ID for cleanup after the session."""

    def _track(job_id: str) -> str:
        _tracked_jobs.append(job_id)
        return job_id

    return _track


@pytest.fixture(scope="session", autouse=True)
def cleanup_jobs(client: AuthenticatedClient, _tracked_jobs: list[str]):
    """Delete all jobs created during the test session."""
    yield
    for job_id in _tracked_jobs:
        with contextlib.suppress(Exception):
            delete_job.sync_detailed(uuid=job_id, client=client)
