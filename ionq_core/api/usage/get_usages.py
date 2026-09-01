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

from ...models.bad_request_error import BadRequestError
from ...models.error import Error
from ...models.group_by import check_group_by
from ...models.group_by import GroupBy
from ...models.modality import check_modality
from ...models.modality import Modality
from ...models.usages import Usages
from typing import cast
import datetime



def _get_kwargs(
    organization_id: str,
    *,
    start_date: datetime.date,
    end_date: datetime.date,
    group_by: GroupBy,
    modality: Modality,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    json_group_by: str = group_by
    params["group_by"] = json_group_by

    json_modality: str = modality
    params["modality"] = json_modality


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/organizations/{organization_id}/usage".format(organization_id=quote(str(organization_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BadRequestError | Error | Usages:
    if response.status_code == 200:
        response_200 = Usages.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    response_default = Error.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BadRequestError | Error | Usages]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    group_by: GroupBy,
    modality: Modality,

) -> Response[BadRequestError | Error | Usages]:
    """ Get usage costs

     Retrieves the costs of a given group type, broken down by the given date modality.

    Args:
        organization_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        group_by (GroupBy): QPU Usage grouping Example: project.
        modality (Modality): Report modality Example: daily.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BadRequestError | Error | Usages]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
start_date=start_date,
end_date=end_date,
group_by=group_by,
modality=modality,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    organization_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    group_by: GroupBy,
    modality: Modality,

) -> BadRequestError | Error | Usages | None:
    """ Get usage costs

     Retrieves the costs of a given group type, broken down by the given date modality.

    Args:
        organization_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        group_by (GroupBy): QPU Usage grouping Example: project.
        modality (Modality): Report modality Example: daily.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BadRequestError | Error | Usages
     """


    return sync_detailed(
        organization_id=organization_id,
client=client,
start_date=start_date,
end_date=end_date,
group_by=group_by,
modality=modality,

    ).parsed

async def asyncio_detailed(
    organization_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    group_by: GroupBy,
    modality: Modality,

) -> Response[BadRequestError | Error | Usages]:
    """ Get usage costs

     Retrieves the costs of a given group type, broken down by the given date modality.

    Args:
        organization_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        group_by (GroupBy): QPU Usage grouping Example: project.
        modality (Modality): Report modality Example: daily.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BadRequestError | Error | Usages]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
start_date=start_date,
end_date=end_date,
group_by=group_by,
modality=modality,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    organization_id: str,
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    group_by: GroupBy,
    modality: Modality,

) -> BadRequestError | Error | Usages | None:
    """ Get usage costs

     Retrieves the costs of a given group type, broken down by the given date modality.

    Args:
        organization_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        group_by (GroupBy): QPU Usage grouping Example: project.
        modality (Modality): Report modality Example: daily.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BadRequestError | Error | Usages
     """


    return (await asyncio_detailed(
        organization_id=organization_id,
client=client,
start_date=start_date,
end_date=end_date,
group_by=group_by,
modality=modality,

    )).parsed
