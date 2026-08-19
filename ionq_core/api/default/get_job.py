# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.multi_circuit_job import MultiCircuitJob
from ...models.qaoa_job import QaoaJob
from ...models.quantum_function_job import QuantumFunctionJob
from ...models.single_circuit_job import SingleCircuitJob
from typing import cast



def _get_kwargs(
    uuid: str,

) -> dict[str, Any]:






    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/{uuid}".format(uuid=quote(str(uuid), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_get_job_response_type_0 = SingleCircuitJob.from_dict(data)



                return componentsschemas_get_job_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_get_job_response_type_1 = MultiCircuitJob.from_dict(data)



                return componentsschemas_get_job_response_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_get_job_response_type_2 = QaoaJob.from_dict(data)



                return componentsschemas_get_job_response_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_get_job_response_type_3 = QuantumFunctionJob.from_dict(data)



            return componentsschemas_get_job_response_type_3

        response_200 = _parse_response_200(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob]:
    """
    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob]
     """


    kwargs = _get_kwargs(
        uuid=uuid,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,

) -> Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob | None:
    """
    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob
     """


    return sync_detailed(
        uuid=uuid,
client=client,

    ).parsed

async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob]:
    """
    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob]
     """


    kwargs = _get_kwargs(
        uuid=uuid,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,

) -> Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob | None:
    """
    Args:
        uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | MultiCircuitJob | QaoaJob | QuantumFunctionJob | SingleCircuitJob
     """


    return (await asyncio_detailed(
        uuid=uuid,
client=client,

    )).parsed
