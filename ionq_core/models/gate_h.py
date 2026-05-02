# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gate_h_gate import check_gate_h_gate
from ..models.gate_h_gate import GateHGate
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GateH")



@_attrs_define
class GateH:
    """ 
        Attributes:
            gate (GateHGate):
            targets (list[int]): The single qubit the gate acts on.
            controls (list[int] | Unset): Optional control qubits.
     """

    gate: GateHGate
    targets: list[int]
    controls: list[int] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets = self.targets



        controls: list[int] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
            "targets": targets,
        })
        if controls is not UNSET:
            field_dict["controls"] = controls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_gate_h_gate(d.pop("gate"))




        targets = cast(list[int], d.pop("targets"))


        controls = cast(list[int], d.pop("controls", UNSET))


        gate_h = cls(
            gate=gate,
            targets=targets,
            controls=controls,
        )

        return gate_h

