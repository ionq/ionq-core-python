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

from ...models.characterization import Characterization
from ...models.get_characterization_backend import check_get_characterization_backend
from ...models.get_characterization_backend import GetCharacterizationBackend
from typing import cast
from uuid import UUID



def _get_kwargs(
    backend: GetCharacterizationBackend,
    uuid: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/backends/{backend}/characterizations/{uuid}".format(backend=quote(str(backend), safe=""),uuid=quote(str(uuid), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Characterization | None:
    if response.status_code == 200:
        response_200 = Characterization.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Characterization]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    backend: GetCharacterizationBackend,
    uuid: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Characterization]:
    """ Get a Characterization

     This endpoint retrieves a characterization.

    Args:
        backend (GetCharacterizationBackend):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Characterization]
     """


    kwargs = _get_kwargs(
        backend=backend,
uuid=uuid,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    backend: GetCharacterizationBackend,
    uuid: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Characterization | None:
    """ Get a Characterization

     This endpoint retrieves a characterization.

    Args:
        backend (GetCharacterizationBackend):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Characterization
     """


    return sync_detailed(
        backend=backend,
uuid=uuid,
client=client,

    ).parsed

async def asyncio_detailed(
    backend: GetCharacterizationBackend,
    uuid: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Characterization]:
    """ Get a Characterization

     This endpoint retrieves a characterization.

    Args:
        backend (GetCharacterizationBackend):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Characterization]
     """


    kwargs = _get_kwargs(
        backend=backend,
uuid=uuid,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    backend: GetCharacterizationBackend,
    uuid: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Characterization | None:
    """ Get a Characterization

     This endpoint retrieves a characterization.

    Args:
        backend (GetCharacterizationBackend):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Characterization
     """


    return (await asyncio_detailed(
        backend=backend,
uuid=uuid,
client=client,

    )).parsed
