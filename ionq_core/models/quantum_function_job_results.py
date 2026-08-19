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






T = TypeVar("T", bound="QuantumFunctionJobResults")



@_attrs_define
class QuantumFunctionJobResults:
    """ Results for quantum-function jobs — a scalar estimator output (`value`) and
    its estimated variance across the shot ensemble (`variance`).

        Attributes:
            value (float | Unset): Scalar value produced by the function — typically the expectation value of the
                observable.
            variance (float | Unset): Estimated variance of `value` across the shot ensemble.
     """

    value: float | Unset = UNSET
    variance: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        value = self.value

        variance = self.variance


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if value is not UNSET:
            field_dict["value"] = value
        if variance is not UNSET:
            field_dict["variance"] = variance

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value", UNSET)

        variance = d.pop("variance", UNSET)

        quantum_function_job_results = cls(
            value=value,
            variance=variance,
        )

        return quantum_function_job_results

