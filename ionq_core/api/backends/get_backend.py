# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.backend import Backend
from ...models.get_backend_backend import check_get_backend_backend
from ...models.get_backend_backend import GetBackendBackend
from typing import cast



def _get_kwargs(
    backend: GetBackendBackend,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/backends/{backend}".format(backend=quote(str(backend), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Backend | None:
    if response.status_code == 200:
        response_200 = Backend.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Backend]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    backend: GetBackendBackend,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Backend]:
    """ Get a Backend

     This endpoint retrieves a backend.

    Args:
        backend (GetBackendBackend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Backend]
     """


    kwargs = _get_kwargs(
        backend=backend,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    backend: GetBackendBackend,
    *,
    client: AuthenticatedClient | Client,

) -> Backend | None:
    """ Get a Backend

     This endpoint retrieves a backend.

    Args:
        backend (GetBackendBackend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Backend
     """


    return sync_detailed(
        backend=backend,
client=client,

    ).parsed

async def asyncio_detailed(
    backend: GetBackendBackend,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Backend]:
    """ Get a Backend

     This endpoint retrieves a backend.

    Args:
        backend (GetBackendBackend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Backend]
     """


    kwargs = _get_kwargs(
        backend=backend,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    backend: GetBackendBackend,
    *,
    client: AuthenticatedClient | Client,

) -> Backend | None:
    """ Get a Backend

     This endpoint retrieves a backend.

    Args:
        backend (GetBackendBackend):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Backend
     """


    return (await asyncio_detailed(
        backend=backend,
client=client,

    )).parsed
