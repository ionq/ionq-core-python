from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_job_probabilities_response_200 import GetJobProbabilitiesResponse200
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    uuid: str,
    *,
    sharpen: bool | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["sharpen"] = sharpen


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/{uuid}/results/probabilities".format(uuid=quote(str(uuid), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | GetJobProbabilitiesResponse200 | None:
    if response.status_code == 200:
        response_200 = GetJobProbabilitiesResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | GetJobProbabilitiesResponse200]:
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
    sharpen: bool | Unset = UNSET,

) -> Response[Any | GetJobProbabilitiesResponse200]:
    """ Fetch the probability distribution for a completed job.

    Args:
        uuid (str):
        sharpen (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobProbabilitiesResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
sharpen=sharpen,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,
    sharpen: bool | Unset = UNSET,

) -> Any | GetJobProbabilitiesResponse200 | None:
    """ Fetch the probability distribution for a completed job.

    Args:
        uuid (str):
        sharpen (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobProbabilitiesResponse200
     """


    return sync_detailed(
        uuid=uuid,
client=client,
sharpen=sharpen,

    ).parsed

async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    sharpen: bool | Unset = UNSET,

) -> Response[Any | GetJobProbabilitiesResponse200]:
    """ Fetch the probability distribution for a completed job.

    Args:
        uuid (str):
        sharpen (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobProbabilitiesResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
sharpen=sharpen,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,
    sharpen: bool | Unset = UNSET,

) -> Any | GetJobProbabilitiesResponse200 | None:
    """ Fetch the probability distribution for a completed job.

    Args:
        uuid (str):
        sharpen (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobProbabilitiesResponse200
     """


    return (await asyncio_detailed(
        uuid=uuid,
client=client,
sharpen=sharpen,

    )).parsed
