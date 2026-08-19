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
  from ..models.registered_probabilities import RegisteredProbabilities





T = TypeVar("T", bound="IonqResultProbabilitiesJsonV2")



@_attrs_define
class IonqResultProbabilitiesJsonV2:
    """ `ionq.result.probabilities.json.v2` — Register-nested probability distribution.
    Each register maps zero-padded bitstrings to probabilities summing to 1 within
    the register.

        Example:
            {'probabilities': {'registers': {'output_all': {'11': 0.5, '00': 0.5}}}}

        Attributes:
            probabilities (RegisteredProbabilities): Per-register probability distributions, keyed by register name.
     """

    probabilities: RegisteredProbabilities





    def to_dict(self) -> dict[str, Any]:
        from ..models.registered_probabilities import RegisteredProbabilities
        probabilities = self.probabilities.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "probabilities": probabilities,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registered_probabilities import RegisteredProbabilities
        d = dict(src_dict)
        probabilities = RegisteredProbabilities.from_dict(d.pop("probabilities"))




        ionq_result_probabilities_json_v2 = cls(
            probabilities=probabilities,
        )

        return ionq_result_probabilities_json_v2

