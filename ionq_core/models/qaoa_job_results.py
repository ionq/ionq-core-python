# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.qaoa_results import QaoaResults





T = TypeVar("T", bound="QaoaJobResults")



@_attrs_define
class QaoaJobResults:
    """ Results for `qctrl.qaoa.v1` jobs.

        Attributes:
            qaoa_results (QaoaResults | Unset): Optimization output recorded by a Q-CTRL QAOA job after it completes.
     """

    qaoa_results: QaoaResults | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.qaoa_results import QaoaResults
        qaoa_results: dict[str, Any] | Unset = UNSET
        if not isinstance(self.qaoa_results, Unset):
            qaoa_results = self.qaoa_results.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if qaoa_results is not UNSET:
            field_dict["qaoa_results"] = qaoa_results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qaoa_results import QaoaResults
        d = dict(src_dict)
        _qaoa_results = d.pop("qaoa_results", UNSET)
        qaoa_results: QaoaResults | Unset
        if isinstance(_qaoa_results,  Unset):
            qaoa_results = UNSET
        else:
            qaoa_results = QaoaResults.from_dict(_qaoa_results)




        qaoa_job_results = cls(
            qaoa_results=qaoa_results,
        )

        return qaoa_job_results

