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
  from ..models.register_probabilities import RegisterProbabilities





T = TypeVar("T", bound="RegisteredProbabilitiesRegisters")



@_attrs_define
class RegisteredProbabilitiesRegisters:
    """ Bitstring → probability map for this register.

     """

    additional_properties: dict[str, RegisterProbabilities] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.register_probabilities import RegisterProbabilities

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.register_probabilities import RegisterProbabilities
        d = dict(src_dict)
        registered_probabilities_registers = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RegisterProbabilities.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        registered_probabilities_registers.additional_properties = additional_properties
        return registered_probabilities_registers

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> RegisterProbabilities:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: RegisterProbabilities) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
