# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Session lifecycle manager for IonQ QPU sessions.

Sessions allow you to reserve priority access to a QPU backend. The
`SessionManager` class wraps the session create / end / status APIs
and supports both sync and async context managers for automatic cleanup.

Example:
    ```python
    from ionq_core import IonQClient, SessionManager

    client = IonQClient()

    # Context manager creates and automatically ends the session
    with SessionManager(client, "qpu.aria-1", max_jobs=10) as session:
        print(session.session_id)
        print(session.status())  # "started"
        # ... submit jobs using session.session_id ...

    # Or reconnect to an existing session
    session = SessionManager.from_id(client, "existing-session-id")
    print(session.status())
    ```
"""

from __future__ import annotations

__all__ = ["SessionManager"]

import logging
from typing import TYPE_CHECKING

from .api.default import create_session, end_session, get_session
from .exceptions import IonQError
from .models.create_session_request import CreateSessionRequest
from .models.session_cost_limit import SessionCostLimit
from .models.session_settings_request import SessionSettingsRequest
from .types import UNSET, Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient

logger = logging.getLogger("ionq_core")


class SessionManager:
    """Convenience wrapper around session create / end / status APIs.

    Can be used as both a sync and async context manager. On exit the
    session is automatically ended. Exceptions during close are logged
    and suppressed so that cleanup does not mask the original error.

    Args:
        client: An authenticated API client.
        backend: The backend to create a session on (e.g. ``"qpu.aria-1"``).
        max_jobs: Optional maximum number of jobs for this session.
        max_time: Optional maximum session duration in minutes.
        max_cost: Optional maximum cost in USD for the session.

    Examples:
        Sync context manager:

        ```python
        with SessionManager(client, "qpu.aria-1", max_jobs=10) as session:
            print(session.session_id)
        ```

        Async context manager:

        ```python
        async with SessionManager(client, "qpu.aria-1") as session:
            print(session.session_id)
        ```
    """

    def __init__(
        self,
        client: AuthenticatedClient,
        backend: str,
        *,
        max_jobs: int | None = None,
        max_time: int | None = None,
        max_cost: float | None = None,
    ) -> None:
        self._client = client
        self._backend = backend
        self._max_jobs = max_jobs
        self._max_time = max_time
        self._max_cost = max_cost
        self._session_id: str | None = None

    @classmethod
    def from_id(cls, client: AuthenticatedClient, session_id: str) -> SessionManager:
        """Reconnect to an existing session without creating a new one.

        This is useful for resuming work with a session that was created
        in a previous process or by another client.

        Args:
            client: An authenticated API client.
            session_id: The ID of the existing session.

        Returns:
            A `SessionManager` bound to the given session ID. The ``backend``
            field will be empty since it is not needed for status checks
            or ending the session.
        """
        mgr = cls(client, backend="")
        mgr._session_id = session_id
        return mgr

    @property
    def session_id(self) -> str | None:
        """The session ID, or ``None`` if `open` has not been called."""
        return self._session_id

    def _build_settings(self) -> SessionSettingsRequest | Unset:
        kw: dict = {}
        if self._max_jobs is not None:
            kw["job_count_limit"] = self._max_jobs
        if self._max_time is not None:
            kw["duration_limit_min"] = self._max_time
        if self._max_cost is not None:
            kw["cost_limit"] = SessionCostLimit(unit="usd", value=self._max_cost)
        return SessionSettingsRequest(**kw) if kw else UNSET

    def open(self) -> None:
        """Create a new session on the configured backend.

        Raises:
            IonQError: If a session is already open or creation fails.
        """
        if self._session_id is not None:
            raise IonQError("Session already open")
        body = CreateSessionRequest(backend=self._backend, settings=self._build_settings())
        session = create_session.sync(client=self._client, body=body)
        if session is None:
            raise IonQError("Failed to create session")
        self._session_id = session.id
        logger.info("Opened session %s", self._session_id)

    def close(self) -> None:
        """End the session. Suppresses exceptions so cleanup is safe."""
        if self._session_id is None:
            return
        try:
            end_session.sync(session_id=self._session_id, client=self._client)
            logger.info("Closed session %s", self._session_id)
        except Exception:
            logger.warning("Failed to end session %s", self._session_id, exc_info=True)

    def status(self) -> str:
        """Get the current session status (e.g. ``"created"``, ``"started"``, ``"ended"``).

        Raises:
            IonQError: If no session is open or the status fetch fails.
        """
        if self._session_id is None:
            raise IonQError("No session ID; call open() first")
        session = get_session.sync(session_id=self._session_id, client=self._client)
        if session is None:
            raise IonQError(f"Failed to fetch session {self._session_id}")
        return session.status

    async def async_open(self) -> None:
        """Async version of `open`."""
        if self._session_id is not None:
            raise IonQError("Session already open")
        body = CreateSessionRequest(backend=self._backend, settings=self._build_settings())
        session = await create_session.asyncio(client=self._client, body=body)
        if session is None:
            raise IonQError("Failed to create session")
        self._session_id = session.id
        logger.info("Opened session %s", self._session_id)

    async def async_close(self) -> None:
        """End the session (async). Suppresses exceptions so cleanup is safe."""
        if self._session_id is None:
            return
        try:
            await end_session.asyncio(session_id=self._session_id, client=self._client)
            logger.info("Closed session %s", self._session_id)
        except Exception:
            logger.warning("Failed to end session %s", self._session_id, exc_info=True)

    async def async_status(self) -> str:
        """Async version of `status`."""
        if self._session_id is None:
            raise IonQError("No session ID; call open() first")
        session = await get_session.asyncio(session_id=self._session_id, client=self._client)
        if session is None:
            raise IonQError(f"Failed to fetch session {self._session_id}")
        return session.status

    def __enter__(self) -> SessionManager:
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    async def __aenter__(self) -> SessionManager:
        await self.async_open()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.async_close()
