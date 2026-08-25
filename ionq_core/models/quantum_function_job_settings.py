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
  from ..models.circuit_job_error_mitigation_settings import CircuitJobErrorMitigationSettings





T = TypeVar("T", bound="QuantumFunctionJobSettings")



@_attrs_define
class QuantumFunctionJobSettings:
    """ Settings for quantum-function-family jobs (`qctrl.qaoa.v1`, `quantum-function`).
    Unlike circuit jobs, no compilation settings are accepted — only error mitigation.

        Attributes:
            error_mitigation (CircuitJobErrorMitigationSettings | Unset):
     """

    error_mitigation: CircuitJobErrorMitigationSettings | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.circuit_job_error_mitigation_settings import CircuitJobErrorMitigationSettings
        error_mitigation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error_mitigation, Unset):
            error_mitigation = self.error_mitigation.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if error_mitigation is not UNSET:
            field_dict["error_mitigation"] = error_mitigation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_job_error_mitigation_settings import CircuitJobErrorMitigationSettings
        d = dict(src_dict)
        _error_mitigation = d.pop("error_mitigation", UNSET)
        error_mitigation: CircuitJobErrorMitigationSettings | Unset
        if isinstance(_error_mitigation,  Unset):
            error_mitigation = UNSET
        else:
            error_mitigation = CircuitJobErrorMitigationSettings.from_dict(_error_mitigation)




        quantum_function_job_settings = cls(
            error_mitigation=error_mitigation,
        )

        return quantum_function_job_settings
