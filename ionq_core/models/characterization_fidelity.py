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
  from ..models.characterization_fidelity_spam import CharacterizationFidelitySpam





T = TypeVar("T", bound="CharacterizationFidelity")



@_attrs_define
class CharacterizationFidelity:
    """ Fidelity for single-qubit (`1q`) and two-qubit (`2q`) gates, and State Preparation and Measurement (`spam`)
    operations.
    Currently provides only median fidelity; additional statistical data will be added in the future.

        Attributes:
            spam (CharacterizationFidelitySpam): SPAM error correction information.
     """

    spam: CharacterizationFidelitySpam
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.characterization_fidelity_spam import CharacterizationFidelitySpam
        spam = self.spam.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "spam": spam,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.characterization_fidelity_spam import CharacterizationFidelitySpam
        d = dict(src_dict)
        spam = CharacterizationFidelitySpam.from_dict(d.pop("spam"))




        characterization_fidelity = cls(
            spam=spam,
        )


        characterization_fidelity.additional_properties = d
        return characterization_fidelity

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
