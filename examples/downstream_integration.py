# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Downstream SDK integration example for the sync ionq-core API."""

from __future__ import annotations

import os
from typing import cast

import httpx

from ionq_core import (
    APIError,
    AuthenticatedClient,
    ClientExtension,
    EventHook,
    IonQClient,
    RateLimitError,
    wait_for_job,
)
from ionq_core.api.default import create_job, get_job_probabilities
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload
from ionq_core.models.get_results_response import GetResultsResponse
from ionq_core.models.job_creation_response import JobCreationResponse


class DownstreamSDKError(RuntimeError):
    """Base exception raised by this example downstream SDK."""


class DownstreamRateLimitError(DownstreamSDKError):
    """Raised when IonQ returns a rate-limit response."""


class LoggingHook(EventHook):
    """Minimal request/response logger for a downstream SDK wrapper."""

    def on_request(self, request: httpx.Request) -> None:
        print(f"sdk -> {request.method} {request.url.path}")

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        print(f"sdk <- {response.status_code} {request.url.path}")


def map_ionq_error(exc: Exception) -> Exception:
    """Convert ionq-core transport exceptions into downstream SDK errors."""
    if isinstance(exc, RateLimitError):
        retry_after = f" Retry after {exc.retry_after}s." if exc.retry_after is not None else ""
        return DownstreamRateLimitError(f"IonQ API rate limit exceeded.{retry_after}")
    if isinstance(exc, APIError):
        return DownstreamSDKError(f"IonQ API request failed: {exc.message}")
    return exc


def bell_state_payload() -> CircuitJobCreationPayload:
    """Build a Bell-state job payload for the simulator backend."""
    return CircuitJobCreationPayload.from_dict(
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


def build_client() -> AuthenticatedClient:
    """Create an IonQ client configured as a downstream SDK would configure it."""
    extension = ClientExtension(
        user_agent_token="example-downstream-sdk/0.1",
        default_headers={"X-Downstream-SDK": "example-sync"},
        event_hooks=(LoggingHook(),),
        error_mapper=map_ionq_error,
    )
    return IonQClient(extension=extension)


def main() -> None:
    if "IONQ_API_KEY" not in os.environ:
        raise SystemExit("Set IONQ_API_KEY before running this example.")

    client = build_client()
    job_response = create_job.sync(client=client, body=bell_state_payload())
    if job_response is None:
        raise DownstreamSDKError("IonQ API did not return a job creation response.")

    job = cast(JobCreationResponse, job_response)
    completed_job = wait_for_job(client, job.id)

    probabilities_response = get_job_probabilities.sync(uuid=completed_job.id, client=client)
    if probabilities_response is None:
        raise DownstreamSDKError(f"IonQ API did not return probabilities for job {completed_job.id}.")

    probabilities = cast(GetResultsResponse, probabilities_response)
    print(probabilities.additional_properties)


if __name__ == "__main__":
    main()
