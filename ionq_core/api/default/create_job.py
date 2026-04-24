# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.circuit_job_creation_payload import CircuitJobCreationPayload
from ...models.job_creation_response import JobCreationResponse
from ...models.json_multi_circuit_job import JSONMultiCircuitJob
from ...models.quantum_function_job_creation_payload import QuantumFunctionJobCreationPayload
from typing import cast



def _get_kwargs(
    *,
    body: CircuitJobCreationPayload | JSONMultiCircuitJob | QuantumFunctionJobCreationPayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/jobs",
    }

    
    if isinstance(body, CircuitJobCreationPayload):
        _kwargs["json"] = body.to_dict()
    elif isinstance(body, JSONMultiCircuitJob):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()



    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | JobCreationResponse | None:
    if response.status_code == 201:
        response_201 = JobCreationResponse.from_dict(response.json())



        return response_201

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if response.status_code == 502:
        response_502 = cast(Any, None)
        return response_502

    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | JobCreationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CircuitJobCreationPayload | JSONMultiCircuitJob | QuantumFunctionJobCreationPayload,

) -> Response[Any | JobCreationResponse]:
    """  Submit a single-circuit or multi-circuit job for simulation or execution. In `ionq.multi-circuit.v1`
    payloads, each entry in `input.circuits` inherits the parent `input.gateset` unless the circuit sets
    its own `gateset`.

    Args:
        body (CircuitJobCreationPayload | JSONMultiCircuitJob |
            QuantumFunctionJobCreationPayload):  Example: {'type': 'ionq.circuit.v1', 'input':
            {'qubits': 1, 'gateset': 'qis', 'circuit': [{'gate': 'h', 'target': 0}]}, 'backend':
            'qpu.forte-1', 'shots': 500, 'settings': {'error_mitigation': {'debiasing': False}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobCreationResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: CircuitJobCreationPayload | JSONMultiCircuitJob | QuantumFunctionJobCreationPayload,

) -> Any | JobCreationResponse | None:
    """  Submit a single-circuit or multi-circuit job for simulation or execution. In `ionq.multi-circuit.v1`
    payloads, each entry in `input.circuits` inherits the parent `input.gateset` unless the circuit sets
    its own `gateset`.

    Args:
        body (CircuitJobCreationPayload | JSONMultiCircuitJob |
            QuantumFunctionJobCreationPayload):  Example: {'type': 'ionq.circuit.v1', 'input':
            {'qubits': 1, 'gateset': 'qis', 'circuit': [{'gate': 'h', 'target': 0}]}, 'backend':
            'qpu.forte-1', 'shots': 500, 'settings': {'error_mitigation': {'debiasing': False}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobCreationResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CircuitJobCreationPayload | JSONMultiCircuitJob | QuantumFunctionJobCreationPayload,

) -> Response[Any | JobCreationResponse]:
    """  Submit a single-circuit or multi-circuit job for simulation or execution. In `ionq.multi-circuit.v1`
    payloads, each entry in `input.circuits` inherits the parent `input.gateset` unless the circuit sets
    its own `gateset`.

    Args:
        body (CircuitJobCreationPayload | JSONMultiCircuitJob |
            QuantumFunctionJobCreationPayload):  Example: {'type': 'ionq.circuit.v1', 'input':
            {'qubits': 1, 'gateset': 'qis', 'circuit': [{'gate': 'h', 'target': 0}]}, 'backend':
            'qpu.forte-1', 'shots': 500, 'settings': {'error_mitigation': {'debiasing': False}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobCreationResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CircuitJobCreationPayload | JSONMultiCircuitJob | QuantumFunctionJobCreationPayload,

) -> Any | JobCreationResponse | None:
    """  Submit a single-circuit or multi-circuit job for simulation or execution. In `ionq.multi-circuit.v1`
    payloads, each entry in `input.circuits` inherits the parent `input.gateset` unless the circuit sets
    its own `gateset`.

    Args:
        body (CircuitJobCreationPayload | JSONMultiCircuitJob |
            QuantumFunctionJobCreationPayload):  Example: {'type': 'ionq.circuit.v1', 'input':
            {'qubits': 1, 'gateset': 'qis', 'circuit': [{'gate': 'h', 'target': 0}]}, 'backend':
            'qpu.forte-1', 'shots': 500, 'settings': {'error_mitigation': {'debiasing': False}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobCreationResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
