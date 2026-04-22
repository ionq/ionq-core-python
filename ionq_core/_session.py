"""Session lifecycle manager for IonQ QPU sessions."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._exceptions import IonQError
from .api.default import create_session, end_session, get_session
from .models.create_session_request import CreateSessionRequest
from .models.session_cost_limit import SessionCostLimit
from .models.session_settings_request import SessionSettingsRequest
from .types import UNSET, Unset

if TYPE_CHECKING:
    from .client import AuthenticatedClient

logger = logging.getLogger("ionq_core")


class SessionManager:
    """Convenience wrapper around session create / end / status APIs.

    Can be used as a context manager to automatically end the session on exit.
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
        """Reconnect to an existing session without creating a new one."""
        mgr = cls(client, backend="")
        mgr._session_id = session_id
        return mgr

    @property
    def session_id(self) -> str | None:
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
        if self._session_id is None:
            raise IonQError("No session ID; call open() first")
        session = get_session.sync(session_id=self._session_id, client=self._client)
        if session is None:
            raise IonQError(f"Failed to fetch session {self._session_id}")
        return session.status

    async def async_open(self) -> None:
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
