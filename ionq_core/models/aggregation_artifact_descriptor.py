# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.result_format_histogram_v2 import check_result_format_histogram_v2
from ..models.result_format_histogram_v2 import ResultFormatHistogramV2
from typing import cast






T = TypeVar("T", bound="AggregationArtifactDescriptor")



@_attrs_define
class AggregationArtifactDescriptor:
    """
        Attributes:
            id (str):
            format_ (ResultFormatHistogramV2):
            media_type (str):
     """

    id: str
    format_: ResultFormatHistogramV2
    media_type: str





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        format_: str = self.format_

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

        format_ = check_result_format_histogram_v2(d.pop("format"))




        media_type = d.pop("media_type")

        aggregation_artifact_descriptor = cls(
            id=id,
            format_=format_,
            media_type=media_type,
        )

        return aggregation_artifact_descriptor
