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
  from ..models.compiled_circuits import CompiledCircuits





T = TypeVar("T", bound="CompilationOutput")



@_attrs_define
class CompilationOutput:
    """ 
        Attributes:
            compiled_circuits (CompiledCircuits | Unset): Map of compiled-circuit artifacts keyed by circuit format
                identifier
                (e.g. `ionq.native.v1`). See the [Circuit formats](/api-reference/v0.4/schemas/circuit-formats) page for the
                catalog of valid identifiers.
     """

    compiled_circuits: CompiledCircuits | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.compiled_circuits import CompiledCircuits
        compiled_circuits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compiled_circuits, Unset):
            compiled_circuits = self.compiled_circuits.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if compiled_circuits is not UNSET:
            field_dict["compiled_circuits"] = compiled_circuits

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_circuits import CompiledCircuits
        d = dict(src_dict)
        _compiled_circuits = d.pop("compiled_circuits", UNSET)
        compiled_circuits: CompiledCircuits | Unset
        if isinstance(_compiled_circuits,  Unset):
            compiled_circuits = UNSET
        else:
            compiled_circuits = CompiledCircuits.from_dict(_compiled_circuits)




        compilation_output = cls(
            compiled_circuits=compiled_circuits,
        )

        return compilation_output
