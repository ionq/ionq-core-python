# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Downstream-SDK integration example (asynchronous).

The async counterpart of ``downstream_integration.py``: the same
``ClientExtension`` integration (user-agent token, default headers, and a
shared ``error_mapper``) but using an ``AsyncEventHook`` and the ``asyncio``
endpoint variants on the async client path.

The script submits a Bell-state circuit to the free ``simulator`` backend,
waits for it to finish, and prints the measured probabilities. See
``examples/README.md`` for setup (install, ``IONQ_API_KEY``) and how to run it.
"""

import asyncio
import logging

import httpx

from ionq_core import (
    APIError,
    AsyncEventHook,
    ClientExtension,
    IonQClient,
    RateLimitError,
    async_wait_for_job,
)
from ionq_core.api.default import create_job, get_job, get_job_probabilities
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

logger = logging.getLogger("downstream_sdk")


# --- Errors the downstream SDK exposes to its own users --------------------


class DownstreamSDKError(Exception):
    """Base error type raised by this example SDK."""


class DownstreamRateLimitError(DownstreamSDKError):
    """Raised when IonQ rate-limits a request."""

    def __init__(self, message: str, *, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


def map_error(exc: Exception) -> Exception:
    """Translate ``ionq-core`` exceptions into SDK-defined error types.

    The mapper is synchronous on both client paths: ``ionq-core`` invokes it
    synchronously even inside the async transport, so the same function serves
    the sync and async examples.
    """
    if isinstance(exc, RateLimitError):
        return DownstreamRateLimitError(f"IonQ rate limit hit: {exc.message}", retry_after=exc.retry_after)
    if isinstance(exc, APIError):
        return DownstreamSDKError(f"IonQ API error {exc.status_code}: {exc.message}")
    return exc


# --- Observability: log every request and response -------------------------


class AsyncLoggingHook(AsyncEventHook):
    """Logs each outgoing request and incoming response (async)."""

    async def on_request(self, request: httpx.Request) -> None:
        logger.info("--> %s %s", request.method, request.url)

    async def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        logger.info("<-- %s %s", response.status_code, request.url)


BELL_STATE = CircuitJobCreationPayload.from_dict(
    {
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "shots": 100,
        "input": {
            "gateset": "qis",
            "qubits": 2,
            "circuit": [
                {"gate": "h", "target": 0},
                {"gate": "cnot", "control": 0, "target": 1},
            ],
        },
    }
)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    extension = ClientExtension(
        user_agent_token="downstream-sdk/1.0.0",
        default_headers={"X-Downstream-SDK": "example"},
        async_event_hooks=(AsyncLoggingHook(),),
        error_mapper=map_error,
    )
    async with IonQClient(extension=extension) as client:  # reads IONQ_API_KEY from the environment
        try:
            job = await create_job.asyncio(client=client, body=BELL_STATE)
            if job is None:
                raise DownstreamSDKError("create_job returned no response body")
            completed = await async_wait_for_job(client, job.id)
            probabilities = await get_job_probabilities.asyncio(uuid=job.id, client=client)
            if probabilities is None:
                raise DownstreamSDKError("get_job_probabilities returned no response body")
            logger.info("job %s finished with status %r", job.id, completed.status)
            print("Bell-state probabilities:", probabilities.additional_properties)
        except DownstreamSDKError:
            logger.exception("downstream SDK call failed")
            raise

        # The error_mapper also covers failures: requesting a job that does not
        # exist returns 404, which ionq-core raises as NotFoundError (an APIError
        # subclass) and map_error converts into a DownstreamSDKError.
        try:
            await get_job.asyncio(uuid="00000000-0000-0000-0000-000000000000", client=client)
        except DownstreamSDKError as exc:
            logger.info("error_mapper converted a failure into: %s", exc)


if __name__ == "__main__":
    asyncio.run(main())
