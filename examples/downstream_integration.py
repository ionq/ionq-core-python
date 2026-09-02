# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Downstream-SDK integration example (synchronous).

Shows how a higher-level SDK can wrap ``ionq-core`` through the extension API
without modifying the library: a ``ClientExtension`` bundle carrying a
user-agent token, default headers, a request/response ``EventHook``, and an
``error_mapper`` that translates ``ionq-core`` exceptions into SDK-defined
error types.

The script submits a Bell-state circuit to the free ``simulator`` backend,
waits for it to finish, and prints the measured probabilities. See
``examples/README.md`` for setup (install, ``IONQ_API_KEY``) and how to run it.
"""

import logging

import httpx

from ionq_core import (
    APIError,
    ClientExtension,
    EventHook,
    IonQClient,
    RateLimitError,
    wait_for_job,
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

    Passed to ``ionq-core`` via ``ClientExtension.error_mapper``. Returning the
    original exception leaves it unchanged; returning a new one makes
    ``ionq-core`` raise that instead (chained from the original).
    """
    if isinstance(exc, RateLimitError):
        return DownstreamRateLimitError(f"IonQ rate limit hit: {exc.message}", retry_after=exc.retry_after)
    if isinstance(exc, APIError):
        return DownstreamSDKError(f"IonQ API error {exc.status_code}: {exc.message}")
    return exc


# --- Observability: log every request and response -------------------------


class LoggingHook(EventHook):
    """Logs each outgoing request and incoming response."""

    def on_request(self, request: httpx.Request) -> None:
        logger.info("--> %s %s", request.method, request.url)

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    extension = ClientExtension(
        user_agent_token="downstream-sdk/1.0.0",
        default_headers={"X-Downstream-SDK": "example"},
        event_hooks=(LoggingHook(),),
        error_mapper=map_error,
    )
    with IonQClient(extension=extension) as client:  # reads IONQ_API_KEY from the environment
        try:
            job = create_job.sync(client=client, body=BELL_STATE)
            if job is None:
                raise DownstreamSDKError("create_job returned no response body")
            completed = wait_for_job(client, job.id)
            probabilities = get_job_probabilities.sync(uuid=job.id, client=client)
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
            get_job.sync(uuid="00000000-0000-0000-0000-000000000000", client=client)
        except DownstreamSDKError as exc:
            logger.info("error_mapper converted a failure into: %s", exc)


if __name__ == "__main__":
    main()
