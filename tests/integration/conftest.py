"""Fixtures for integration tests against the real IonQ API."""

import contextlib
import os
import warnings

import pytest

from ionq_core import AuthenticatedClient, IonQClient
from ionq_core.api.default import delete_job


@pytest.fixture(scope="session", autouse=True)
def _suppress_ssl_teardown_warnings():
    """Suppress harmless SSL socket warnings during process teardown."""
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*SSL")
    warnings.filterwarnings("ignore", category=pytest.PytestUnraisableExceptionWarning, message=".*SSL.*")


_job_ids: list[str] = []


@pytest.fixture(scope="session")
def api_key() -> str:
    key = os.environ.get("IONQ_API_KEY")
    if not key:
        pytest.skip("IONQ_API_KEY not set")
    return key


@pytest.fixture(scope="session")
def client(api_key: str) -> AuthenticatedClient:
    return IonQClient(api_key=api_key)


@pytest.fixture
def track_job():
    """Register a job ID for cleanup after the session."""

    def _track(job_id: str) -> str:
        _job_ids.append(job_id)
        return job_id

    return _track


@pytest.fixture(scope="session", autouse=True)
def cleanup_jobs(client: AuthenticatedClient):
    """Delete all jobs created during the test session."""
    yield
    for job_id in _job_ids:
        with contextlib.suppress(Exception):
            delete_job.sync_detailed(uuid=job_id, client=client)
