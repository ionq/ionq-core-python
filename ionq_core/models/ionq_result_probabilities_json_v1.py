# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="IonqResultProbabilitiesJsonV1")



@_attrs_define
class IonqResultProbabilitiesJsonV1:
    """ `ionq.result.probabilities.json.v1` — Legacy probability distribution.
    Flat object keyed by decimal qubit state integer strings, values are
    probabilities summing to 1.

        Example:
            {'0': 0.5, '1': 0.25, '3': 0.25}

     """

    additional_properties: dict[str, float] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ionq_result_probabilities_json_v1 = cls(
        )


        ionq_result_probabilities_json_v1.additional_properties = d
        return ionq_result_probabilities_json_v1

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> float:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: float) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
