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






T = TypeVar("T", bound="ErrorMitigationOutputSymmetryVerificationType0")



@_attrs_define
class ErrorMitigationOutputSymmetryVerificationType0:
    """ 
        Attributes:
            num_allowed_states (float | Unset):
            applied (bool | Unset):
     """

    num_allowed_states: float | Unset = UNSET
    applied: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        num_allowed_states = self.num_allowed_states

        applied = self.applied


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if num_allowed_states is not UNSET:
            field_dict["num_allowed_states"] = num_allowed_states
        if applied is not UNSET:
            field_dict["applied"] = applied

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        num_allowed_states = d.pop("num_allowed_states", UNSET)

        applied = d.pop("applied", UNSET)

        error_mitigation_output_symmetry_verification_type_0 = cls(
            num_allowed_states=num_allowed_states,
            applied=applied,
        )


        error_mitigation_output_symmetry_verification_type_0.additional_properties = d
        return error_mitigation_output_symmetry_verification_type_0

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
