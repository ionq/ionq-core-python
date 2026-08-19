# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ArtifactDescriptor")



@_attrs_define
class ArtifactDescriptor:
    """ Artifact descriptor. Pass `id` to `GET /v0.4/jobs/{id}/artifacts/{artifactId}` to
    download the artifact payload, then validate it against the JSON Schema for its format.

        Attributes:
            id (str): Artifact ID used to download via the artifacts endpoint.
            format_ (str): Format identifier. Fetch the payload schema from the matching schema-catalog endpoint.
            media_type (str):
     """

    id: str
    format_: str
    media_type: str





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        format_ = self.format_

        media_type = self.media_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "format": format_,
            "media_type": media_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        format_ = d.pop("format")

        media_type = d.pop("media_type")

        artifact_descriptor = cls(
            id=id,
            format_=format_,
            media_type=media_type,
        )

        return artifact_descriptor
