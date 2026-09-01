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
  from ..models.aggregation_artifact_descriptor import AggregationArtifactDescriptor





T = TypeVar("T", bound="AggregationsOutput")



@_attrs_define
class AggregationsOutput:
    """ 
        Attributes:
            average (AggregationArtifactDescriptor | Unset):
            voting (AggregationArtifactDescriptor | Unset):
            dnl (AggregationArtifactDescriptor | Unset):
            majority (AggregationArtifactDescriptor | Unset):
     """

    average: AggregationArtifactDescriptor | Unset = UNSET
    voting: AggregationArtifactDescriptor | Unset = UNSET
    dnl: AggregationArtifactDescriptor | Unset = UNSET
    majority: AggregationArtifactDescriptor | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.aggregation_artifact_descriptor import AggregationArtifactDescriptor
        average: dict[str, Any] | Unset = UNSET
        if not isinstance(self.average, Unset):
            average = self.average.to_dict()

        voting: dict[str, Any] | Unset = UNSET
        if not isinstance(self.voting, Unset):
            voting = self.voting.to_dict()

        dnl: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dnl, Unset):
            dnl = self.dnl.to_dict()

        majority: dict[str, Any] | Unset = UNSET
        if not isinstance(self.majority, Unset):
            majority = self.majority.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if average is not UNSET:
            field_dict["average"] = average
        if voting is not UNSET:
            field_dict["voting"] = voting
        if dnl is not UNSET:
            field_dict["dnl"] = dnl
        if majority is not UNSET:
            field_dict["majority"] = majority

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregation_artifact_descriptor import AggregationArtifactDescriptor
        d = dict(src_dict)
        _average = d.pop("average", UNSET)
        average: AggregationArtifactDescriptor | Unset
        if isinstance(_average,  Unset):
            average = UNSET
        else:
            average = AggregationArtifactDescriptor.from_dict(_average)




        _voting = d.pop("voting", UNSET)
        voting: AggregationArtifactDescriptor | Unset
        if isinstance(_voting,  Unset):
            voting = UNSET
        else:
            voting = AggregationArtifactDescriptor.from_dict(_voting)




        _dnl = d.pop("dnl", UNSET)
        dnl: AggregationArtifactDescriptor | Unset
        if isinstance(_dnl,  Unset):
            dnl = UNSET
        else:
            dnl = AggregationArtifactDescriptor.from_dict(_dnl)




        _majority = d.pop("majority", UNSET)
        majority: AggregationArtifactDescriptor | Unset
        if isinstance(_majority,  Unset):
            majority = UNSET
        else:
            majority = AggregationArtifactDescriptor.from_dict(_majority)




        aggregations_output = cls(
            average=average,
            voting=voting,
            dnl=dnl,
            majority=majority,
        )

        return aggregations_output

