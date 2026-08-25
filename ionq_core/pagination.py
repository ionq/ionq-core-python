# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pagination helpers for cursor-based IonQ API endpoints.

Each helper wraps a raw endpoint call, follows the ``next`` cursor, and yields individual jobs.

Example:
    ```python
    from ionq_core import IonQClient, iter_jobs

    client = IonQClient()
    for job in iter_jobs(client, status="completed"):
        print(job.id)
    ```
"""

from __future__ import annotations

__all__ = ["aiter_jobs", "aiter_session_jobs", "iter_jobs", "iter_session_jobs"]

import logging
from collections.abc import AsyncIterator, Callable, Iterator
from typing import TYPE_CHECKING, Any

from .api.default import get_jobs, get_session_jobs
from .exceptions import IonQError
from .types import UNSET, Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient
    from .models.base_job import BaseJob as Job
    from .models.job_status import JobStatus

logger = logging.getLogger("ionq_core")


def _check_cursor(cursor: str, seen: set[str], label: str) -> None:
    # The server-controlled cursor is the loop's only exit condition: empty or repeated means abort, not loop forever.
    if not cursor or cursor in seen:
        raise IonQError(f"Pagination cursor for {label} did not advance (next={cursor!r}); aborting")
    seen.add(cursor)


def _paginate(fetch: Callable[..., Any], label: str, *args: Any, **kwargs: Any) -> Iterator[Job]:
    kwargs["next_"] = UNSET
    seen_cursors: set[str] = set()
    while True:
        response = fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        yield from response.jobs
        if response.next_ is None:
            return
        _check_cursor(response.next_, seen_cursors, label)
        kwargs["next_"] = response.next_
        logger.debug("Fetching next page of %s (cursor=%s)", label, response.next_)


async def _apaginate(fetch: Callable[..., Any], label: str, *args: Any, **kwargs: Any) -> AsyncIterator[Job]:
    kwargs["next_"] = UNSET
    seen_cursors: set[str] = set()
    while True:
        response = await fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        for job in response.jobs:
            yield job
        if response.next_ is None:
            return
        _check_cursor(response.next_, seen_cursors, label)
        kwargs["next_"] = response.next_
        logger.debug("Fetching next page of %s (cursor=%s)", label, response.next_)


def iter_jobs(
    client: AuthenticatedClient,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Iterator[Job]:
    """Iterate over all jobs, following pagination cursors.

    Args:
        client: An authenticated API client.
        status: Filter by job status.
        target: Filter by backend target name.
        session_id: Filter by session ID.
        submitter_id: Filter by submitter user ID.
        limit: Jobs per page, not a total cap; the server default applies if unset.

    Yields:
        Job objects across all pages.

    Raises:
        IonQError: If the API returns ``None``, or if the cursor is empty or repeats, which would loop forever.
    """
    return _paginate(
        get_jobs.sync,
        "jobs",
        client=client,
        status=status,
        target=target,
        session_id=session_id,
        submitter_id=submitter_id,
        limit=limit,
    )


def aiter_jobs(
    client: AuthenticatedClient,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> AsyncIterator[Job]:
    """Async version of `iter_jobs`."""
    return _apaginate(
        get_jobs.asyncio,
        "jobs",
        client=client,
        status=status,
        target=target,
        session_id=session_id,
        submitter_id=submitter_id,
        limit=limit,
    )


def iter_session_jobs(
    client: AuthenticatedClient,
    session_id: str,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Iterator[Job]:
    """Like `iter_jobs`, but scoped to one session.

    Args:
        client: An authenticated API client.
        session_id: The session to list jobs for.
        status: Filter by job status.
        target: Filter by backend target name.
        submitter_id: Filter by submitter user ID.
        limit: Jobs per page, not a total cap; the server default applies if unset.

    Yields:
        Job objects across all pages.

    Raises:
        IonQError: If the API returns ``None``, or if the cursor is empty or repeats, which would loop forever.
    """
    return _paginate(
        get_session_jobs.sync,
        "session jobs",
        session_id,
        client=client,
        status=status,
        target=target,
        submitter_id=submitter_id,
        limit=limit,
    )


def aiter_session_jobs(
    client: AuthenticatedClient,
    session_id: str,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> AsyncIterator[Job]:
    """Async version of `iter_session_jobs`."""
    return _apaginate(
        get_session_jobs.asyncio,
        "session jobs",
        session_id,
        client=client,
        status=status,
        target=target,
        submitter_id=submitter_id,
        limit=limit,
    )
