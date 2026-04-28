# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_job_estimate_response import GetJobEstimateResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    backend: str,
    type_: str | Unset = 'ionq.circuit.v1',
    qubits: int | Unset = 25,
    shots: int | Unset = 1000,
    field_1q_gates: int | Unset = 0,
    field_2q_gates: int | Unset = 0,
    error_mitigation: bool | Unset = False,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["backend"] = backend

    params["type"] = type_

    params["qubits"] = qubits

    params["shots"] = shots

    params["1q_gates"] = field_1q_gates

    params["2q_gates"] = field_2q_gates

    params["error_mitigation"] = error_mitigation


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/estimate",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | GetJobEstimateResponse | None:
    if response.status_code == 200:
        response_200 = GetJobEstimateResponse.from_dict(response.json())



        return response_200

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | GetJobEstimateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    backend: str,
    type_: str | Unset = 'ionq.circuit.v1',
    qubits: int | Unset = 25,
    shots: int | Unset = 1000,
    field_1q_gates: int | Unset = 0,
    field_2q_gates: int | Unset = 0,
    error_mitigation: bool | Unset = False,

) -> Response[Any | GetJobEstimateResponse]:
    """ 
    Args:
        backend (str): Available options: `simulator`, `qpu.aria-1`, `qpu.aria-2`, `qpu.forte-1`,
            `qpu.forte-enterprise-1`
        type_ (str | Unset):  Default: 'ionq.circuit.v1'.
        qubits (int | Unset):  Default: 25.
        shots (int | Unset):  Default: 1000.
        field_1q_gates (int | Unset):  Default: 0.
        field_2q_gates (int | Unset):  Default: 0.
        error_mitigation (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobEstimateResponse]
     """


    kwargs = _get_kwargs(
        backend=backend,
type_=type_,
qubits=qubits,
shots=shots,
field_1q_gates=field_1q_gates,
field_2q_gates=field_2q_gates,
error_mitigation=error_mitigation,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    backend: str,
    type_: str | Unset = 'ionq.circuit.v1',
    qubits: int | Unset = 25,
    shots: int | Unset = 1000,
    field_1q_gates: int | Unset = 0,
    field_2q_gates: int | Unset = 0,
    error_mitigation: bool | Unset = False,

) -> Any | GetJobEstimateResponse | None:
    """ 
    Args:
        backend (str): Available options: `simulator`, `qpu.aria-1`, `qpu.aria-2`, `qpu.forte-1`,
            `qpu.forte-enterprise-1`
        type_ (str | Unset):  Default: 'ionq.circuit.v1'.
        qubits (int | Unset):  Default: 25.
        shots (int | Unset):  Default: 1000.
        field_1q_gates (int | Unset):  Default: 0.
        field_2q_gates (int | Unset):  Default: 0.
        error_mitigation (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobEstimateResponse
     """


    return sync_detailed(
        client=client,
backend=backend,
type_=type_,
qubits=qubits,
shots=shots,
field_1q_gates=field_1q_gates,
field_2q_gates=field_2q_gates,
error_mitigation=error_mitigation,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    backend: str,
    type_: str | Unset = 'ionq.circuit.v1',
    qubits: int | Unset = 25,
    shots: int | Unset = 1000,
    field_1q_gates: int | Unset = 0,
    field_2q_gates: int | Unset = 0,
    error_mitigation: bool | Unset = False,

) -> Response[Any | GetJobEstimateResponse]:
    """ 
    Args:
        backend (str): Available options: `simulator`, `qpu.aria-1`, `qpu.aria-2`, `qpu.forte-1`,
            `qpu.forte-enterprise-1`
        type_ (str | Unset):  Default: 'ionq.circuit.v1'.
        qubits (int | Unset):  Default: 25.
        shots (int | Unset):  Default: 1000.
        field_1q_gates (int | Unset):  Default: 0.
        field_2q_gates (int | Unset):  Default: 0.
        error_mitigation (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobEstimateResponse]
     """


    kwargs = _get_kwargs(
        backend=backend,
type_=type_,
qubits=qubits,
shots=shots,
field_1q_gates=field_1q_gates,
field_2q_gates=field_2q_gates,
error_mitigation=error_mitigation,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    backend: str,
    type_: str | Unset = 'ionq.circuit.v1',
    qubits: int | Unset = 25,
    shots: int | Unset = 1000,
    field_1q_gates: int | Unset = 0,
    field_2q_gates: int | Unset = 0,
    error_mitigation: bool | Unset = False,

) -> Any | GetJobEstimateResponse | None:
    """ 
    Args:
        backend (str): Available options: `simulator`, `qpu.aria-1`, `qpu.aria-2`, `qpu.forte-1`,
            `qpu.forte-enterprise-1`
        type_ (str | Unset):  Default: 'ionq.circuit.v1'.
        qubits (int | Unset):  Default: 25.
        shots (int | Unset):  Default: 1000.
        field_1q_gates (int | Unset):  Default: 0.
        field_2q_gates (int | Unset):  Default: 0.
        error_mitigation (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobEstimateResponse
     """


    return (await asyncio_detailed(
        client=client,
backend=backend,
type_=type_,
qubits=qubits,
shots=shots,
field_1q_gates=field_1q_gates,
field_2q_gates=field_2q_gates,
error_mitigation=error_mitigation,

    )).parsed
