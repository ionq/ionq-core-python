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
  from ..models.compilation_output import CompilationOutput
  from ..models.error_mitigation_output import ErrorMitigationOutput





T = TypeVar("T", bound="CircuitJobOutput")



@_attrs_define
class CircuitJobOutput:
    """ 
        Attributes:
            compilation (CompilationOutput | Unset):
            error_mitigation (ErrorMitigationOutput | Unset):
     """

    compilation: CompilationOutput | Unset = UNSET
    error_mitigation: ErrorMitigationOutput | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.compilation_output import CompilationOutput
        from ..models.error_mitigation_output import ErrorMitigationOutput
        compilation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compilation, Unset):
            compilation = self.compilation.to_dict()

        error_mitigation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error_mitigation, Unset):
            error_mitigation = self.error_mitigation.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if compilation is not UNSET:
            field_dict["compilation"] = compilation
        if error_mitigation is not UNSET:
            field_dict["error_mitigation"] = error_mitigation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compilation_output import CompilationOutput
        from ..models.error_mitigation_output import ErrorMitigationOutput
        d = dict(src_dict)
        _compilation = d.pop("compilation", UNSET)
        compilation: CompilationOutput | Unset
        if isinstance(_compilation,  Unset):
            compilation = UNSET
        else:
            compilation = CompilationOutput.from_dict(_compilation)




        _error_mitigation = d.pop("error_mitigation", UNSET)
        error_mitigation: ErrorMitigationOutput | Unset
        if isinstance(_error_mitigation,  Unset):
            error_mitigation = UNSET
        else:
            error_mitigation = ErrorMitigationOutput.from_dict(_error_mitigation)




        circuit_job_output = cls(
            compilation=compilation,
            error_mitigation=error_mitigation,
        )


        circuit_job_output.additional_properties = d
        return circuit_job_output

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
