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






T = TypeVar("T", bound="FormatSchemaDocument")



@_attrs_define
class FormatSchemaDocument:
    """ JSON Schema document returned by the schemas endpoint. The exact contents
    vary by format identifier (see the Results / Circuit formats catalog
    pages for each format's structure).

        Attributes:
            schema (str): JSON Schema draft URI.
            id (str): Format identifier (matches the path parameter).
            type_ (str): Top-level JSON type of the format payload.
            description (str | Unset): Human-readable description of the format.
     """

    schema: str
    id: str
    type_: str
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        id = self.id

        type_ = self.type_

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "$schema": schema,
            "$id": id,
            "type": type_,
        })
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema")

        id = d.pop("$id")

        type_ = d.pop("type")

        description = d.pop("description", UNSET)

        format_schema_document = cls(
            schema=schema,
            id=id,
            type_=type_,
            description=description,
        )


        format_schema_document.additional_properties = d
        return format_schema_document

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
