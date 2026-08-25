# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Job polling helpers.

`wait_for_job` (or `async_wait_for_job`) blocks until a job reaches a terminal state, polling with backoff.

Example:
    ```python
    from ionq_core import IonQClient, wait_for_job
    from ionq_core.api.default import create_job

    client = IonQClient()
    job = create_job.sync(client=client, body=payload)
    completed = wait_for_job(client, job.id, timeout=300)
    print(completed.status)  # "completed"
    ```
"""

from __future__ import annotations

__all__ = ["JobFailedError", "JobTimeoutError", "async_wait_for_job", "wait_for_job"]

import asyncio
import logging
import time
from typing import TYPE_CHECKING

from .api.default import get_job
from .exceptions import IonQError
from .types import Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient
    from .models.get_job_response import GetJobResponse

logger = logging.getLogger("ionq_core")

_TERMINAL = frozenset({"completed", "failed", "canceled"})
_DEFAULT_INTERVAL = 1.0
_DEFAULT_TIMEOUT = 300.0
_MAX_INTERVAL = 30.0
_BACKOFF_FACTOR = 1.5


class JobTimeoutError(IonQError):
    """Raised when a job does not reach a terminal state within the timeout.

    Attributes:
        job_id: The job that timed out.
        timeout: The exceeded timeout, in seconds.
        last_status: Last status seen before the timeout, e.g. ``"submitted"``.
    """

    def __init__(self, job_id: str, timeout: float, last_status: str) -> None:
        self.job_id = job_id
        self.timeout = timeout
        self.last_status = last_status
        super().__init__(f"Job {job_id} did not complete within {timeout}s (last status: {last_status})")


class JobFailedError(IonQError):
    """Raised when a polled job reaches ``"failed"`` status.

    Attributes:
        job_id: The failed job.
        failure: Failure detail from the API response, or ``None`` if the response carried none.
    """

    def __init__(self, job_id: str, failure: object) -> None:
        self.job_id = job_id
        self.failure = failure
        super().__init__(f"Job {job_id} failed: {failure}")


def _check_terminal(job: GetJobResponse, raise_on_failure: bool) -> bool:
    if raise_on_failure and job.status == "failed":
        raise JobFailedError(job.id, None if isinstance(job.failure, Unset) else job.failure)
    return job.status in _TERMINAL


def wait_for_job(
    client: AuthenticatedClient,
    job_id: str,
    *,
    poll_interval: float = _DEFAULT_INTERVAL,
    timeout: float = _DEFAULT_TIMEOUT,
    raise_on_failure: bool = True,
) -> GetJobResponse:
    """Poll a job until it reaches a terminal state.

    Terminal states are ``"completed"``, ``"failed"``, and ``"canceled"``.
    Polling backs off 1.5x per attempt, capped at 30 seconds.

    Args:
        client: An authenticated API client.
        job_id: The UUID of the job to poll.
        poll_interval: Seconds before the first re-poll. Defaults to 1.0.
        timeout: Maximum total wait, in seconds. Defaults to 300.
        raise_on_failure: Raise `JobFailedError` on a ``"failed"`` status. If ``False``, return the failed response.

    Returns:
        The job response in its terminal state.

    Raises:
        JobTimeoutError: If the job does not finish within ``timeout``.
        JobFailedError: If ``raise_on_failure`` and the job fails.
        IonQError: If the API returns ``None``.
    """
    deadline = time.monotonic() + timeout
    interval = poll_interval
    while True:
        job = get_job.sync(uuid=job_id, client=client)
        if job is None:
            raise IonQError(f"Failed to fetch job {job_id}")
        logger.debug("Job %s status: %s", job_id, job.status)
        if _check_terminal(job, raise_on_failure):
            return job
        if time.monotonic() >= deadline:
            raise JobTimeoutError(job_id, timeout, job.status)
        time.sleep(max(0, min(interval, deadline - time.monotonic())))
        interval = min(interval * _BACKOFF_FACTOR, _MAX_INTERVAL)


async def async_wait_for_job(
    client: AuthenticatedClient,
    job_id: str,
    *,
    poll_interval: float = _DEFAULT_INTERVAL,
    timeout: float = _DEFAULT_TIMEOUT,
    raise_on_failure: bool = True,
) -> GetJobResponse:
    """Async version of `wait_for_job`.

    Args:
        client: An authenticated API client.
        job_id: The UUID of the job to poll.
        poll_interval: Seconds before the first re-poll. Defaults to 1.0.
        timeout: Maximum total wait, in seconds. Defaults to 300.
        raise_on_failure: Raise `JobFailedError` on a ``"failed"`` status.

    Returns:
        The job response in its terminal state.

    Raises:
        JobTimeoutError: If the job does not finish within ``timeout``.
        JobFailedError: If ``raise_on_failure`` and the job fails.
        IonQError: If the API returns ``None``.
    """
    deadline = time.monotonic() + timeout
    interval = poll_interval
    while True:
        job = await get_job.asyncio(uuid=job_id, client=client)
        if job is None:
            raise IonQError(f"Failed to fetch job {job_id}")
        logger.debug("Job %s status: %s", job_id, job.status)
        if _check_terminal(job, raise_on_failure):
            return job
        if time.monotonic() >= deadline:
            raise JobTimeoutError(job_id, timeout, job.status)
        await asyncio.sleep(max(0, min(interval, deadline - time.monotonic())))
        interval = min(interval * _BACKOFF_FACTOR, _MAX_INTERVAL)
