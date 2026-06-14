# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Sync downstream-SDK example: ClientExtension + Bell state on simulator.

Shows how a higher-level SDK wraps ionq-core with ``user_agent_token``,
``default_headers``, an ``EventHook``, and an ``error_mapper`` that translates
``APIError`` / ``RateLimitError`` into SDK-defined exception types.

Extension API reference:
https://ionq.github.io/ionq-core-python/ionq_core/extensions.html
"""

from __future__ import annotations

import logging
import sys

import httpx

from ionq_core import APIError, ClientExtension, EventHook, IonQClient, RateLimitError, wait_for_job
from ionq_core.api.default import create_job, get_job_probabilities
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

SDK_NAME = "example-sdk/0.1.0"
logger = logging.getLogger(__name__)

BELL_CIRCUIT = CircuitJobCreationPayload.from_dict(
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


class ExampleSDKError(Exception):
    """Base exception for this example downstream SDK."""


class ExampleAPIError(ExampleSDKError):
    """SDK wrapper around ionq-core HTTP API errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(message)


class ExampleRateLimitError(ExampleAPIError):
    """SDK wrapper around ionq-core rate-limit errors."""

    def __init__(self, message: str, *, retry_after: float | None = None) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429)


class LoggingHook(EventHook):
    """Sync event hook: log requests, responses, and transport failures."""

    def on_request(self, request: httpx.Request) -> None:
        logger.info("--> %s %s", request.method, request.url)

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        logger.info("<-- %s %s", response.status_code, request.url)

    def on_error(self, request: httpx.Request, error: Exception) -> None:
        logger.warning("!! %s %s failed: %s", request.method, request.url, error)


def map_ionq_error(exc: Exception) -> Exception:
    if isinstance(exc, RateLimitError):
        return ExampleRateLimitError(f"IonQ rate limit: {exc.message}", retry_after=exc.retry_after)
    if isinstance(exc, APIError):
        return ExampleAPIError(
            f"IonQ API {exc.status_code}: {exc.message}",
            status_code=exc.status_code,
            request_id=exc.request_id,
        )
    return exc


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)

    extension = ClientExtension(
        user_agent_token=SDK_NAME,
        default_headers={"X-Example-SDK": SDK_NAME},
        event_hooks=(LoggingHook(),),
        error_mapper=map_ionq_error,
    )

    try:
        with IonQClient(extension=extension) as client:
            job = create_job.sync(client=client, body=BELL_CIRCUIT)
            if job is None:
                raise ExampleSDKError("create_job returned no job")

            completed = wait_for_job(client, job.id, timeout=120)
            probs = get_job_probabilities.sync(uuid=job.id, client=client)
            if probs is None:
                raise ExampleSDKError(f"get_job_probabilities returned no data for job {job.id}")

            print()
            print("Bell-state job on simulator")
            print(f"  job_id:  {completed.id}")
            print(f"  status:  {completed.status}")
            print(f"  results: {probs.additional_properties}")
    except ExampleSDKError:
        logger.exception("downstream SDK call failed")
        return 1
    except ValueError as exc:
        logger.error("%s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
