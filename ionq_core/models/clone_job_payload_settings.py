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
  from ..models.clone_job_payload_settings_compilation import CloneJobPayloadSettingsCompilation
  from ..models.clone_job_payload_settings_error_mitigation import CloneJobPayloadSettingsErrorMitigation





T = TypeVar("T", bound="CloneJobPayloadSettings")



@_attrs_define
class CloneJobPayloadSettings:
    """ 
        Attributes:
            error_mitigation (CloneJobPayloadSettingsErrorMitigation | Unset):
            compilation (CloneJobPayloadSettingsCompilation | Unset):
     """

    error_mitigation: CloneJobPayloadSettingsErrorMitigation | Unset = UNSET
    compilation: CloneJobPayloadSettingsCompilation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.clone_job_payload_settings_compilation import CloneJobPayloadSettingsCompilation
        from ..models.clone_job_payload_settings_error_mitigation import CloneJobPayloadSettingsErrorMitigation
        error_mitigation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error_mitigation, Unset):
            error_mitigation = self.error_mitigation.to_dict()

        compilation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compilation, Unset):
            compilation = self.compilation.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if error_mitigation is not UNSET:
            field_dict["error_mitigation"] = error_mitigation
        if compilation is not UNSET:
            field_dict["compilation"] = compilation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.clone_job_payload_settings_compilation import CloneJobPayloadSettingsCompilation
        from ..models.clone_job_payload_settings_error_mitigation import CloneJobPayloadSettingsErrorMitigation
        d = dict(src_dict)
        _error_mitigation = d.pop("error_mitigation", UNSET)
        error_mitigation: CloneJobPayloadSettingsErrorMitigation | Unset
        if isinstance(_error_mitigation,  Unset):
            error_mitigation = UNSET
        else:
            error_mitigation = CloneJobPayloadSettingsErrorMitigation.from_dict(_error_mitigation)




        _compilation = d.pop("compilation", UNSET)
        compilation: CloneJobPayloadSettingsCompilation | Unset
        if isinstance(_compilation,  Unset):
            compilation = UNSET
        else:
            compilation = CloneJobPayloadSettingsCompilation.from_dict(_compilation)




        clone_job_payload_settings = cls(
            error_mitigation=error_mitigation,
            compilation=compilation,
        )


        clone_job_payload_settings.additional_properties = d
        return clone_job_payload_settings

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
