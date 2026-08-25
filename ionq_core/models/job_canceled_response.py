# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_canceled_response_status import check_job_canceled_response_status
from ..models.job_canceled_response_status import JobCanceledResponseStatus
from typing import cast






T = TypeVar("T", bound="JobCanceledResponse")



@_attrs_define
class JobCanceledResponse:
    """ 
        Attributes:
            id (str):  Example: 617a1f8b-59d4-435d-aa33-695433d7155e.
            status (JobCanceledResponseStatus):
     """

    id: str
    status: JobCanceledResponseStatus





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status: str = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = check_job_canceled_response_status(d.pop("status"))




        job_canceled_response = cls(
            id=id,
            status=status,
        )

        return job_canceled_response
