# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Synchronous downstream-SDK integration example.

This script demonstrates how a downstream SDK can use the ionq-core extension
API to add SDK-specific headers, a User-Agent token, sync HTTP event logging,
and error mapping while submitting a Bell-state circuit to the simulator.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

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


class ExampleSDKError(Exception):
    """Exception type that a downstream SDK might expose to its users."""


class LoggingHook(EventHook):
    """Minimal sync event hook used by the example SDK."""

    def on_request(self, request: httpx.Request) -> None:
        print(f"example-sdk -> {request.method} {request.url}")

    def on_response(self, request: httpx.Request, response: httpx.Response) -> None:
        print(f"example-sdk <- {response.status_code} {request.method} {request.url.path}")

    def on_error(self, request: httpx.Request, error: Exception) -> None:
        print(f"example-sdk !! {request.method} {request.url.path}: {error}")


def map_ionq_error(error: Exception) -> Exception:
    """Translate ionq-core API errors into a downstream SDK exception."""
    if isinstance(error, RateLimitError):
        return ExampleSDKError(f"IonQ rate limit exceeded; retry after {error.retry_after!r} seconds")
    if isinstance(error, APIError):
        return ExampleSDKError(f"IonQ API request failed: {error.message}")
    return error


def example_sdk_client() -> AuthenticatedClient:
    """Build an IonQ client configured as a downstream SDK would configure it."""
    return IonQClient(
        extension=ClientExtension(
            user_agent_token="example-sdk/0.1",
            default_headers={"X-Example-SDK": "sync"},
            event_hooks=(LoggingHook(),),
            error_mapper=map_ionq_error,
        )
    )


def bell_state_payload() -> CircuitJobCreationPayload:
    """Build the Bell-state job payload used by the example."""
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


def run_bell_state(client: AuthenticatedClient) -> Mapping[str, float]:
    """Submit a Bell-state job, wait for completion, and fetch probabilities."""
    created = create_job.sync(client=client, body=bell_state_payload())
    if created is None:
        raise ExampleSDKError("IonQ API did not return a job creation response")

    completed = wait_for_job(client, created.id)
    probabilities = get_job_probabilities.sync(uuid=completed.id, client=client)
    if probabilities is None:
        raise ExampleSDKError("IonQ API did not return probabilities")
    return probabilities.additional_properties


def main() -> None:
    """Run the sync downstream integration example."""
    client = example_sdk_client()
    try:
        probabilities: Mapping[str, Any] = run_bell_state(client)
        print(dict(probabilities))
    finally:
        client.get_httpx_client().close()


if __name__ == "__main__":
    main()
