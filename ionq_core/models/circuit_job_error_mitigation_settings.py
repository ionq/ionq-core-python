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






T = TypeVar("T", bound="CircuitJobErrorMitigationSettings")



@_attrs_define
class CircuitJobErrorMitigationSettings:
    """ 
        Attributes:
            debiasing (bool | Unset):
            symmetry_verification (bool | Unset):
     """

    debiasing: bool | Unset = UNSET
    symmetry_verification: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        debiasing = self.debiasing

        symmetry_verification = self.symmetry_verification


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if debiasing is not UNSET:
            field_dict["debiasing"] = debiasing
        if symmetry_verification is not UNSET:
            field_dict["symmetry_verification"] = symmetry_verification

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        debiasing = d.pop("debiasing", UNSET)

        symmetry_verification = d.pop("symmetry_verification", UNSET)

        circuit_job_error_mitigation_settings = cls(
            debiasing=debiasing,
            symmetry_verification=symmetry_verification,
        )

        return circuit_job_error_mitigation_settings

