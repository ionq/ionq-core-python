# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SessionCostLimit")



@_attrs_define
class SessionCostLimit:
    """ 
        Attributes:
            unit (str):
            value (float):
     """

    unit: str
    value: float





    def to_dict(self) -> dict[str, Any]:
        unit = self.unit

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "unit": unit,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unit = d.pop("unit")

        value = d.pop("value")

        session_cost_limit = cls(
            unit=unit,
            value=value,
        )

        return session_cost_limit

