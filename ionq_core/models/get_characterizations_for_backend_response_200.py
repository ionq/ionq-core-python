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
  from ..models.characterization import Characterization





T = TypeVar("T", bound="GetCharacterizationsForBackendResponse200")



@_attrs_define
class GetCharacterizationsForBackendResponse200:
    """ Response body from requesting characterization data.

        Attributes:
            characterizations (list[Characterization]): A page of characterizations measurements.
            pages (int | Unset): The number of remaining pages of characterization measurements.
     """

    characterizations: list[Characterization]
    pages: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.characterization import Characterization
        characterizations = []
        for characterizations_item_data in self.characterizations:
            characterizations_item = characterizations_item_data.to_dict()
            characterizations.append(characterizations_item)



        pages = self.pages


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "characterizations": characterizations,
        })
        if pages is not UNSET:
            field_dict["pages"] = pages

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.characterization import Characterization
        d = dict(src_dict)
        characterizations = []
        _characterizations = d.pop("characterizations")
        for characterizations_item_data in (_characterizations):
            characterizations_item = Characterization.from_dict(characterizations_item_data)



            characterizations.append(characterizations_item)


        pages = d.pop("pages", UNSET)

        get_characterizations_for_backend_response_200 = cls(
            characterizations=characterizations,
            pages=pages,
        )


        get_characterizations_for_backend_response_200.additional_properties = d
        return get_characterizations_for_backend_response_200

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
