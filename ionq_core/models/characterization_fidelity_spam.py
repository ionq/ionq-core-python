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






T = TypeVar("T", bound="CharacterizationFidelitySpam")



@_attrs_define
class CharacterizationFidelitySpam:
    """ SPAM error correction information.

        Attributes:
            median (float):  Example: 0.9962.
            stderr (int | Unset): SPAM error.
     """

    median: float
    stderr: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        median = self.median

        stderr = self.stderr


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "median": median,
        })
        if stderr is not UNSET:
            field_dict["stderr"] = stderr

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        median = d.pop("median")

        stderr = d.pop("stderr", UNSET)

        characterization_fidelity_spam = cls(
            median=median,
            stderr=stderr,
        )


        characterization_fidelity_spam.additional_properties = d
        return characterization_fidelity_spam

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
