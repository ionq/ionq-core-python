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

if TYPE_CHECKING:
  from ..models.register_histogram import RegisterHistogram





T = TypeVar("T", bound="RegisteredHistogramRegisters")



@_attrs_define
class RegisteredHistogramRegisters:
    """ Per-register shot counts, keyed by register name.

     """

    additional_properties: dict[str, RegisterHistogram] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.register_histogram import RegisterHistogram
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.register_histogram import RegisterHistogram
        d = dict(src_dict)
        registered_histogram_registers = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RegisterHistogram.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        registered_histogram_registers.additional_properties = additional_properties
        return registered_histogram_registers

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> RegisterHistogram:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: RegisterHistogram) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
