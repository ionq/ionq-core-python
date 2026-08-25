# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from http import HTTPStatus
from typing import Any, cast
from ..._url import quote_path_param

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.format_schema_document import FormatSchemaDocument
from ...models.formats import check_formats
from ...models.formats import Formats
from typing import cast



def _get_kwargs(
    format_: Formats,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/schemas/formats/{format_}".format(format_=quote_path_param(format_),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FormatSchemaDocument | None:
    if response.status_code == 200:
        response_200 = FormatSchemaDocument.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FormatSchemaDocument]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    format_: Formats,
    *,
    client: AuthenticatedClient,

) -> Response[FormatSchemaDocument]:
    """  Returns the JSON Schema document for the requested artifact format.
    See the Results formats and Circuit formats catalog pages for the full list of identifiers and their
    payload schemas.

    Args:
        format_ (Formats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormatSchemaDocument]
     """


    kwargs = _get_kwargs(
        format_=format_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    format_: Formats,
    *,
    client: AuthenticatedClient,

) -> FormatSchemaDocument | None:
    """  Returns the JSON Schema document for the requested artifact format.
    See the Results formats and Circuit formats catalog pages for the full list of identifiers and their
    payload schemas.

    Args:
        format_ (Formats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormatSchemaDocument
     """


    return sync_detailed(
        format_=format_,
client=client,

    ).parsed

async def asyncio_detailed(
    format_: Formats,
    *,
    client: AuthenticatedClient,

) -> Response[FormatSchemaDocument]:
    """  Returns the JSON Schema document for the requested artifact format.
    See the Results formats and Circuit formats catalog pages for the full list of identifiers and their
    payload schemas.

    Args:
        format_ (Formats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormatSchemaDocument]
     """


    kwargs = _get_kwargs(
        format_=format_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    format_: Formats,
    *,
    client: AuthenticatedClient,

) -> FormatSchemaDocument | None:
    """  Returns the JSON Schema document for the requested artifact format.
    See the Results formats and Circuit formats catalog pages for the full list of identifiers and their
    payload schemas.

    Args:
        format_ (Formats):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormatSchemaDocument
     """


    return (await asyncio_detailed(
        format_=format_,
client=client,

    )).parsed
