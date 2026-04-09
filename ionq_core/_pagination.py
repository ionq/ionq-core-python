"""Pagination helpers for cursor-based IonQ API endpoints."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING

from .api.default import get_jobs, get_session_jobs
from .types import UNSET, Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient
    from .models.job import Job
    from .models.job_status import JobStatus

logger = logging.getLogger("ionq_core")


def iter_jobs(
    client: AuthenticatedClient,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Iterator[Job]:
    """Iterate over all jobs, automatically following pagination cursors."""
    next_cursor: str | Unset = UNSET
    while True:
        response = get_jobs.sync(
            client=client,
            status=status,
            target=target,
            session_id=session_id,
            submitter_id=submitter_id,
            limit=limit,
            next_=next_cursor,
        )
        if response is None:
            return
        yield from response.jobs
        if response.next_ is None:
            return
        next_cursor = response.next_
        logger.debug("Fetching next page of jobs (cursor=%s)", next_cursor)


async def aiter_jobs(
    client: AuthenticatedClient,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    session_id: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> AsyncIterator[Job]:
    """Async iterate over all jobs, automatically following pagination cursors."""
    next_cursor: str | Unset = UNSET
    while True:
        response = await get_jobs.asyncio(
            client=client,
            status=status,
            target=target,
            session_id=session_id,
            submitter_id=submitter_id,
            limit=limit,
            next_=next_cursor,
        )
        if response is None:
            return
        for job in response.jobs:
            yield job
        if response.next_ is None:
            return
        next_cursor = response.next_
        logger.debug("Fetching next page of jobs (cursor=%s)", next_cursor)


def iter_session_jobs(
    client: AuthenticatedClient,
    session_id: str,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Iterator[Job]:
    """Iterate over all jobs in a session, automatically following pagination cursors."""
    next_cursor: str | Unset = UNSET
    while True:
        response = get_session_jobs.sync(
            session_id,
            client=client,
            status=status,
            target=target,
            submitter_id=submitter_id,
            limit=limit,
            next_=next_cursor,
        )
        if response is None:
            return
        yield from response.jobs
        if response.next_ is None:
            return
        next_cursor = response.next_
        logger.debug("Fetching next page of session jobs (cursor=%s)", next_cursor)


async def aiter_session_jobs(
    client: AuthenticatedClient,
    session_id: str,
    *,
    status: JobStatus | Unset = UNSET,
    target: str | Unset = UNSET,
    submitter_id: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> AsyncIterator[Job]:
    """Async iterate over all jobs in a session, automatically following pagination cursors."""
    next_cursor: str | Unset = UNSET
    while True:
        response = await get_session_jobs.asyncio(
            session_id,
            client=client,
            status=status,
            target=target,
            submitter_id=submitter_id,
            limit=limit,
            next_=next_cursor,
        )
        if response is None:
            return
        for job in response.jobs:
            yield job
        if response.next_ is None:
            return
        next_cursor = response.next_
        logger.debug("Fetching next page of session jobs (cursor=%s)", next_cursor)
