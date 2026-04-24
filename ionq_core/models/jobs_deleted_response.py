# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.jobs_deleted_response_status import check_jobs_deleted_response_status
from ..models.jobs_deleted_response_status import JobsDeletedResponseStatus
from typing import cast






T = TypeVar("T", bound="JobsDeletedResponse")



@_attrs_define
class JobsDeletedResponse:
    """ 
        Attributes:
            ids (list[str]):
            status (JobsDeletedResponseStatus):
     """

    ids: list[str]
    status: JobsDeletedResponseStatus





    def to_dict(self) -> dict[str, Any]:
        ids = self.ids



        status: str = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ids": ids,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = cast(list[str], d.pop("ids"))


        status = check_jobs_deleted_response_status(d.pop("status"))




        jobs_deleted_response = cls(
            ids=ids,
            status=status,
        )

        return jobs_deleted_response

