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






T = TypeVar("T", bound="CloneJobPayloadSettingsErrorMitigation")



@_attrs_define
class CloneJobPayloadSettingsErrorMitigation:
    """
        Attributes:
            symmetry_verification (bool | Unset):
            debiasing (bool | Unset):
     """

    symmetry_verification: bool | Unset = UNSET
    debiasing: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        symmetry_verification = self.symmetry_verification

        debiasing = self.debiasing


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if symmetry_verification is not UNSET:
            field_dict["symmetry_verification"] = symmetry_verification
        if debiasing is not UNSET:
            field_dict["debiasing"] = debiasing

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symmetry_verification = d.pop("symmetry_verification", UNSET)

        debiasing = d.pop("debiasing", UNSET)

        clone_job_payload_settings_error_mitigation = cls(
            symmetry_verification=symmetry_verification,
            debiasing=debiasing,
        )


        clone_job_payload_settings_error_mitigation.additional_properties = d
        return clone_job_payload_settings_error_mitigation

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
