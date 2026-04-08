from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="Whoami")



@_attrs_define
class Whoami:
    """ Details of current API Key session.

        Attributes:
            key_id (UUID): UUID of a API key. Example: e060759f-4348-4767-a645-8c0301265791.
            key_name (str): key name. Example: My First Key.
            project_id (UUID | Unset): UUID of a project. Example: 944904d6-2e30-4cfb-8bc4-04afaabcdd42.
     """

    key_id: UUID
    key_name: str
    project_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        key_id = str(self.key_id)

        key_name = self.key_name

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "key_id": key_id,
            "key_name": key_name,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_id = UUID(d.pop("key_id"))




        key_name = d.pop("key_name")

        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        whoami = cls(
            key_id=key_id,
            key_name=key_name,
            project_id=project_id,
        )


        whoami.additional_properties = d
        return whoami

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
