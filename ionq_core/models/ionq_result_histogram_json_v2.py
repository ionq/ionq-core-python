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
  from ..models.registered_histogram import RegisteredHistogram





T = TypeVar("T", bound="IonqResultHistogramJsonV2")



@_attrs_define
class IonqResultHistogramJsonV2:
    """ `ionq.result.histogram.json.v2` — Register-nested shot count histogram.
    Each register maps zero-padded bitstrings to shot counts.

        Example:
            {'histogram': {'registers': {'output_all': {'11': 500, '00': 500}}}}

        Attributes:
            histogram (RegisteredHistogram): Per-register histogram counts.
     """

    histogram: RegisteredHistogram





    def to_dict(self) -> dict[str, Any]:
        from ..models.registered_histogram import RegisteredHistogram
        histogram = self.histogram.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "histogram": histogram,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registered_histogram import RegisteredHistogram
        d = dict(src_dict)
        histogram = RegisteredHistogram.from_dict(d.pop("histogram"))




        ionq_result_histogram_json_v2 = cls(
            histogram=histogram,
        )

        return ionq_result_histogram_json_v2
