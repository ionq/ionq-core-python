"""Pagination helpers for cursor-based IonQ API endpoints."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Callable, Iterator
from typing import TYPE_CHECKING, Any

from ._exceptions import IonQError
from .api.default import get_jobs, get_session_jobs
from .types import UNSET, Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient
    from .models.base_job import BaseJob as Job
    from .models.job_status import JobStatus

logger = logging.getLogger("ionq_core")


def _paginate(fetch: Callable[..., Any], label: str, *args: Any, **kwargs: Any) -> Iterator[Job]:
    kwargs["next_"] = UNSET
    while True:
        response = fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        yield from response.jobs
        if response.next_ is None:
            return
        kwargs["next_"] = response.next_
        logger.debug("Fetching next page of %s (cursor=%s)", label, response.next_)


async def _apaginate(fetch: Callable[..., Any], label: str, *args: Any, **kwargs: Any) -> AsyncIterator[Job]:
    kwargs["next_"] = UNSET
    while True:
        response = await fetch(*args, **kwargs)
        if response is None:
            raise IonQError(f"Failed to fetch {label}")
        for job in response.jobs:
            yield job
        if response.next_ is None:
            return
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
