# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="JobsBulkOperationRequest")



@_attrs_define
class JobsBulkOperationRequest:
    """ 
        Attributes:
            ids (list[str]):
     """

    ids: list[str]





    def to_dict(self) -> dict[str, Any]:
        ids = self.ids




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ids": ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = cast(list[str], d.pop("ids"))


        jobs_bulk_operation_request = cls(
            ids=ids,
        )

        return jobs_bulk_operation_request
