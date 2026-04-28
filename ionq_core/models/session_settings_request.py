# Copyright 2026 IonQ, Inc.
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
  from ..models.session_cost_limit import SessionCostLimit





T = TypeVar("T", bound="SessionSettingsRequest")



@_attrs_define
class SessionSettingsRequest:
    """ 
        Attributes:
            job_count_limit (int | Unset):
            duration_limit_min (int | Unset):
            cost_limit (SessionCostLimit | Unset):
     """

    job_count_limit: int | Unset = UNSET
    duration_limit_min: int | Unset = UNSET
    cost_limit: SessionCostLimit | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.session_cost_limit import SessionCostLimit
        job_count_limit = self.job_count_limit

        duration_limit_min = self.duration_limit_min

        cost_limit: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cost_limit, Unset):
            cost_limit = self.cost_limit.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if job_count_limit is not UNSET:
            field_dict["job_count_limit"] = job_count_limit
        if duration_limit_min is not UNSET:
            field_dict["duration_limit_min"] = duration_limit_min
        if cost_limit is not UNSET:
            field_dict["cost_limit"] = cost_limit

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_cost_limit import SessionCostLimit
        d = dict(src_dict)
        job_count_limit = d.pop("job_count_limit", UNSET)

        duration_limit_min = d.pop("duration_limit_min", UNSET)

        _cost_limit = d.pop("cost_limit", UNSET)
        cost_limit: SessionCostLimit | Unset
        if isinstance(_cost_limit,  Unset):
            cost_limit = UNSET
        else:
            cost_limit = SessionCostLimit.from_dict(_cost_limit)




        session_settings_request = cls(
            job_count_limit=job_count_limit,
            duration_limit_min=duration_limit_min,
            cost_limit=cost_limit,
        )

        return session_settings_request

