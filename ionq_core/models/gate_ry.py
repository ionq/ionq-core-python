# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gate_ry_gate import check_gate_ry_gate
from ..models.gate_ry_gate import GateRyGate
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GateRy")



@_attrs_define
class GateRy:
    """ 
        Attributes:
            gate (GateRyGate):
            targets (list[int]): The single qubit the gate acts on.
            rotation (float): Rotation angle in radians.
            controls (list[int] | Unset): Optional control qubits.
     """

    gate: GateRyGate
    targets: list[int]
    rotation: float
    controls: list[int] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets = self.targets



        rotation = self.rotation

        controls: list[int] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
            "targets": targets,
            "rotation": rotation,
        })
        if controls is not UNSET:
            field_dict["controls"] = controls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_gate_ry_gate(d.pop("gate"))




        targets = cast(list[int], d.pop("targets"))


        rotation = d.pop("rotation")

        controls = cast(list[int], d.pop("controls", UNSET))


        gate_ry = cls(
            gate=gate,
            targets=targets,
            rotation=rotation,
            controls=controls,
        )

        return gate_ry

