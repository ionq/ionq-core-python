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
  from ..models.child_circuit_probabilities import ChildCircuitProbabilities





T = TypeVar("T", bound="IonqResultProbabilitiesAggregateJsonV1")



@_attrs_define
class IonqResultProbabilitiesAggregateJsonV1:
    """ `ionq.result.probabilities-aggregate.json.v1` — Aggregated probability
    distributions across all circuits in an `ionq.multi-circuit.v1` job. Top-level
    keys are child job UUIDs; each value is that child's probability distribution.

        Example:
            {'06a2099c-f845-7208-8000-8111ee2dccbc': {'2': 1}, '06a2099c-f846-7d32-8000-5726853513db': {'0': 0.5, '1': 0.5}}

     """

    additional_properties: dict[str, ChildCircuitProbabilities] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.child_circuit_probabilities import ChildCircuitProbabilities
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.child_circuit_probabilities import ChildCircuitProbabilities
        d = dict(src_dict)
        ionq_result_probabilities_aggregate_json_v1 = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ChildCircuitProbabilities.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        ionq_result_probabilities_aggregate_json_v1.additional_properties = additional_properties
        return ionq_result_probabilities_aggregate_json_v1

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ChildCircuitProbabilities:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ChildCircuitProbabilities) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
