# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pagination helpers for cursor-based IonQ API endpoints.

The IonQ API returns paginated results with a ``next`` cursor. The helpers
in this module wrap the raw endpoint calls and automatically follow cursors,
yielding individual job objects.

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

DEFAULT_MAX_PAGES: int = 10_000
"""Default page cap for the pagination helpers.

The ``next`` cursor is entirely server-controlled, so without a cap a
misbehaving server that always returns a cursor could force the client to
fetch pages forever. Pass ``max_pages=None`` to opt out.
"""


def _next_cursor(response: Any, label: str, sent_cursor: Any, pages: int, max_pages: int | None) -> None | str:
    """Validate the cursor of a fetched page and return it (``None`` = done)."""
    cursor = response.next_
    if cursor is None:
        return None
    if cursor == sent_cursor:
        raise IonQError(f"Server repeated pagination cursor {cursor!r} while fetching {label}")
    if max_pages is not None and pages >= max_pages:
        raise IonQError(
            f"{label} pagination exceeded max_pages={max_pages}; pass a larger max_pages (or None to disable the cap)"
        )
    logger.debug("Fetching next page of %s (cursor=%s)", label, cursor)
    return cursor


def _paginate(
    fetch: Callable[..., Any], label: str, *args: Any, max_pages: int | None = DEFAULT_MAX_PAGES, **kwargs: Any
) -> Iterator[Job]:
    kwargs["next_"] = UNSET
    pages = 0
    while True:
        response = fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        pages += 1
        yield from response.jobs
        cursor = _next_cursor(response, label, kwargs["next_"], pages, max_pages)
        if cursor is None:
            return
        kwargs["next_"] = cursor


async def _apaginate(
    fetch: Callable[..., Any], label: str, *args: Any, max_pages: int | None = DEFAULT_MAX_PAGES, **kwargs: Any
) -> AsyncIterator[Job]:
    kwargs["next_"] = UNSET
    pages = 0
    while True:
        response = await fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        pages += 1
        for job in response.jobs:
            yield job
        cursor = _next_cursor(response, label, kwargs["next_"], pages, max_pages)
        if cursor is None:
            return
        kwargs["next_"] = cursor


def iter_jobs(
    client: AuthenticatedClient,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    max_pages: int | None = DEFAULT_MAX_PAGES,
) -> Iterator[Job]:
    """Iterate over all jobs, automatically following pagination cursors.

    Args:
        client: An authenticated API client.
        status: Filter by job status (e.g. ``"completed"``, ``"failed"``).
        target: Filter by backend target name.
        session_id: Filter by session ID.
        submitter_id: Filter by submitter user ID.
        limit: Maximum number of jobs per page (server default applies
            if unset).
        max_pages: Maximum number of pages to fetch before raising, as a
            guard against a server that never stops returning cursors.
            Defaults to `DEFAULT_MAX_PAGES` (10,000); pass ``None`` to
            disable the cap.

    Yields:
        Individual job objects across all pages.

    Raises:
        IonQError: If the API returns a ``None`` response, repeats a
            pagination cursor, or exceeds ``max_pages``.
    """
    return _paginate(
        get_jobs.sync,
        "jobs",
        max_pages=max_pages,
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
    max_pages: int | None = DEFAULT_MAX_PAGES,
) -> AsyncIterator[Job]:
    """Async version of `iter_jobs`.

    Args:
        client: An authenticated API client.
        status: Filter by job status.
        target: Filter by backend target name.
        session_id: Filter by session ID.
        submitter_id: Filter by submitter user ID.
        limit: Maximum number of jobs per page.
        max_pages: Maximum number of pages to fetch before raising.
            Defaults to `DEFAULT_MAX_PAGES` (10,000); ``None`` disables
            the cap.

    Yields:
        Individual job objects across all pages.

    Raises:
        IonQError: If the API returns a ``None`` response, repeats a
            pagination cursor, or exceeds ``max_pages``.
    """
    return _apaginate(
        get_jobs.asyncio,
        "jobs",
        max_pages=max_pages,
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
    max_pages: int | None = DEFAULT_MAX_PAGES,
) -> Iterator[Job]:
    """Iterate over all jobs in a specific session.

    Like `iter_jobs`, but scoped to a single session.

    Args:
        client: An authenticated API client.
        session_id: The session ID to list jobs for.
        status: Filter by job status.
        target: Filter by backend target name.
        submitter_id: Filter by submitter user ID.
        limit: Maximum number of jobs per page.
        max_pages: Maximum number of pages to fetch before raising.
            Defaults to `DEFAULT_MAX_PAGES` (10,000); ``None`` disables
            the cap.

    Yields:
        Individual job objects across all pages.

    Raises:
        IonQError: If the API returns a ``None`` response, repeats a
            pagination cursor, or exceeds ``max_pages``.
    """
    return _paginate(
        get_session_jobs.sync,
        "session jobs",
        session_id,
        max_pages=max_pages,
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
    max_pages: int | None = DEFAULT_MAX_PAGES,
) -> AsyncIterator[Job]:
    """Async version of `iter_session_jobs`.

    Args:
        client: An authenticated API client.
        session_id: The session ID to list jobs for.
        status: Filter by job status.
        target: Filter by backend target name.
        submitter_id: Filter by submitter user ID.
        limit: Maximum number of jobs per page.
        max_pages: Maximum number of pages to fetch before raising.
            Defaults to `DEFAULT_MAX_PAGES` (10,000); ``None`` disables
            the cap.

    Yields:
        Individual job objects across all pages.

    Raises:
        IonQError: If the API returns a ``None`` response, repeats a
            pagination cursor, or exceeds ``max_pages``.
    """
    return _apaginate(
        get_session_jobs.asyncio,
        "session jobs",
        session_id,
        max_pages=max_pages,
        client=client,
        status=status,
        target=target,
        submitter_id=submitter_id,
        limit=limit,
    )
