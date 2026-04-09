"""Job polling helpers for waiting on quantum job completion."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING

from ._exceptions import IonQError
from .api.default import get_job

if TYPE_CHECKING:
    from .client import AuthenticatedClient
    from .models.get_job_response import GetJobResponse

logger = logging.getLogger("ionq_core")

_TERMINAL_STATUSES = frozenset({"completed", "failed", "canceled"})
_DEFAULT_POLL_INTERVAL = 1.0
_DEFAULT_TIMEOUT = 300.0
_MAX_POLL_INTERVAL = 30.0


class JobTimeoutError(IonQError):
    """Raised when a job does not reach a terminal state within the timeout."""

    def __init__(self, job_id: str, timeout: float, last_status: str) -> None:
        self.job_id = job_id
        self.timeout = timeout
        self.last_status = last_status
        super().__init__(f"Job {job_id} did not complete within {timeout}s (last status: {last_status})")


class JobFailedError(IonQError):
    """Raised when a polled job reaches 'failed' status."""

    def __init__(self, job_id: str, failure: object) -> None:
        self.job_id = job_id
        self.failure = failure
        super().__init__(f"Job {job_id} failed: {failure}")


def _check_terminal(
    job: GetJobResponse,
    job_id: str,
    raise_on_failure: bool,
) -> GetJobResponse | None:
    """Return the job if it reached a terminal state, else None."""
    if job.status not in _TERMINAL_STATUSES:
        return None
    if raise_on_failure and job.status == "failed":
        raise JobFailedError(job_id, getattr(job, "failure", None))
    return job


def wait_for_job(
    client: AuthenticatedClient,
    job_id: str,
    *,
    poll_interval: float = _DEFAULT_POLL_INTERVAL,
    timeout: float = _DEFAULT_TIMEOUT,
    raise_on_failure: bool = True,
) -> GetJobResponse:
    """Poll a job until it reaches a terminal state (completed, failed, canceled).

    Args:
        client: Authenticated IonQ client.
        job_id: The UUID of the job to poll.
        poll_interval: Initial seconds between polls. Backs off up to 30s.
        timeout: Max seconds to wait before raising JobTimeoutError.
        raise_on_failure: If True, raise JobFailedError when job status is 'failed'.

    Returns:
        The final GetJobResponse.

    Raises:
        JobTimeoutError: If the job does not finish within the timeout.
        JobFailedError: If raise_on_failure is True and the job fails.
    """
    deadline = time.monotonic() + timeout
    interval = poll_interval

    while True:
        job = get_job.sync(uuid=job_id, client=client)
        if job is None:
            raise IonQError(f"Failed to fetch job {job_id}")

        logger.debug("Job %s status: %s", job_id, job.status)

        result = _check_terminal(job, job_id, raise_on_failure)
        if result is not None:
            return result

        if time.monotonic() >= deadline:
            raise JobTimeoutError(job_id, timeout, job.status)

        time.sleep(max(0, min(interval, deadline - time.monotonic())))
        interval = min(interval * 1.5, _MAX_POLL_INTERVAL)


async def async_wait_for_job(
    client: AuthenticatedClient,
    job_id: str,
    *,
    poll_interval: float = _DEFAULT_POLL_INTERVAL,
    timeout: float = _DEFAULT_TIMEOUT,
    raise_on_failure: bool = True,
) -> GetJobResponse:
    """Async version of wait_for_job."""
    deadline = time.monotonic() + timeout
    interval = poll_interval

    while True:
        job = await get_job.asyncio(uuid=job_id, client=client)
        if job is None:
            raise IonQError(f"Failed to fetch job {job_id}")

        logger.debug("Job %s status: %s", job_id, job.status)

        result = _check_terminal(job, job_id, raise_on_failure)
        if result is not None:
            return result

        if time.monotonic() >= deadline:
            raise JobTimeoutError(job_id, timeout, job.status)

        await asyncio.sleep(max(0, min(interval, deadline - time.monotonic())))
        interval = min(interval * 1.5, _MAX_POLL_INTERVAL)
