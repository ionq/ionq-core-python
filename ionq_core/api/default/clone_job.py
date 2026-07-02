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

from ...models.clone_job_payload import CloneJobPayload
from ...models.job_creation_response import JobCreationResponse
from typing import cast



def _get_kwargs(
    uuid: str,
    *,
    body: CloneJobPayload,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/jobs/{uuid}/clone".format(uuid=quote(str(uuid), safe=""),),
    }

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
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: CloneJobPayload,

) -> Response[Any | JobCreationResponse]:
    """ 
    Args:
        uuid (str):
        body (CloneJobPayload): Make all properties in T optional

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobCreationResponse]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: CloneJobPayload,

) -> Any | JobCreationResponse | None:
    """ 
    Args:
        uuid (str):
        body (CloneJobPayload): Make all properties in T optional

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobCreationResponse
     """


    return sync_detailed(
        uuid=uuid,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: CloneJobPayload,

) -> Response[Any | JobCreationResponse]:
    """ 
    Args:
        uuid (str):
        body (CloneJobPayload): Make all properties in T optional

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobCreationResponse]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: CloneJobPayload,

) -> Any | JobCreationResponse | None:
    """ 
    Args:
        uuid (str):
        body (CloneJobPayload): Make all properties in T optional

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobCreationResponse
     """


    return (await asyncio_detailed(
        uuid=uuid,
client=client,
body=body,

    )).parsed
