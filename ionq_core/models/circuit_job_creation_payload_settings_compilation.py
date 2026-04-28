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






T = TypeVar("T", bound="CircuitJobCreationPayloadSettingsCompilation")



@_attrs_define
class CircuitJobCreationPayloadSettingsCompilation:
    """ 
        Attributes:
            opt (float | Unset):
            precision (str | Unset):
     """

    opt: float | Unset = UNSET
    precision: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        opt = self.opt

        precision = self.precision


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if opt is not UNSET:
            field_dict["opt"] = opt
        if precision is not UNSET:
            field_dict["precision"] = precision

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        opt = d.pop("opt", UNSET)

        precision = d.pop("precision", UNSET)

        circuit_job_creation_payload_settings_compilation = cls(
            opt=opt,
            precision=precision,
        )


        circuit_job_creation_payload_settings_compilation.additional_properties = d
        return circuit_job_creation_payload_settings_compilation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
