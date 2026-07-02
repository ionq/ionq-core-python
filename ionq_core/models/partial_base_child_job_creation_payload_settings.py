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
  from ..models.partial_base_child_job_creation_payload_settings_compilation import PartialBaseChildJobCreationPayloadSettingsCompilation
  from ..models.partial_base_child_job_creation_payload_settings_error_mitigation import PartialBaseChildJobCreationPayloadSettingsErrorMitigation





T = TypeVar("T", bound="PartialBaseChildJobCreationPayloadSettings")



@_attrs_define
class PartialBaseChildJobCreationPayloadSettings:
    """ 
        Attributes:
            error_mitigation (PartialBaseChildJobCreationPayloadSettingsErrorMitigation | Unset):
            compilation (PartialBaseChildJobCreationPayloadSettingsCompilation | Unset):
     """

    error_mitigation: PartialBaseChildJobCreationPayloadSettingsErrorMitigation | Unset = UNSET
    compilation: PartialBaseChildJobCreationPayloadSettingsCompilation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.partial_base_child_job_creation_payload_settings_compilation import PartialBaseChildJobCreationPayloadSettingsCompilation
        from ..models.partial_base_child_job_creation_payload_settings_error_mitigation import PartialBaseChildJobCreationPayloadSettingsErrorMitigation
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
        from ..models.partial_base_child_job_creation_payload_settings_compilation import PartialBaseChildJobCreationPayloadSettingsCompilation
        from ..models.partial_base_child_job_creation_payload_settings_error_mitigation import PartialBaseChildJobCreationPayloadSettingsErrorMitigation
        d = dict(src_dict)
        _error_mitigation = d.pop("error_mitigation", UNSET)
        error_mitigation: PartialBaseChildJobCreationPayloadSettingsErrorMitigation | Unset
        if isinstance(_error_mitigation,  Unset):
            error_mitigation = UNSET
        else:
            error_mitigation = PartialBaseChildJobCreationPayloadSettingsErrorMitigation.from_dict(_error_mitigation)




        _compilation = d.pop("compilation", UNSET)
        compilation: PartialBaseChildJobCreationPayloadSettingsCompilation | Unset
        if isinstance(_compilation,  Unset):
            compilation = UNSET
        else:
            compilation = PartialBaseChildJobCreationPayloadSettingsCompilation.from_dict(_compilation)




        partial_base_child_job_creation_payload_settings = cls(
            error_mitigation=error_mitigation,
            compilation=compilation,
        )


        partial_base_child_job_creation_payload_settings.additional_properties = d
        return partial_base_child_job_creation_payload_settings

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
