# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.native_gate import check_native_gate
from ..models.native_gate import NativeGate
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GateNativeGate")



@_attrs_define
class GateNativeGate:
    """ 
        Attributes:
            gate (NativeGate):
            target (int | Unset):
            targets (list[float] | Unset): The qubits that a quantum gate is applied to
            controls (list[float] | Unset): The qubits that determine whether the operation is applied to targets.
            phase (float | Unset): Phase for gpi/gpi2 gates
            phases (list[float] | Unset): Phases for ms gate
            angle (float | Unset): Interaction angle for ms gate (in turns, default 0.25)
            rotation (float | Unset): Rotation angle for rx/ry/rz gates
     """

    gate: NativeGate
    target: int | Unset = UNSET
    targets: list[float] | Unset = UNSET
    controls: list[float] | Unset = UNSET
    phase: float | Unset = UNSET
    phases: list[float] | Unset = UNSET
    angle: float | Unset = UNSET
    rotation: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        target = self.target

        targets: list[float] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = self.targets



        controls: list[float] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls



        phase = self.phase

        phases: list[float] | Unset = UNSET
        if not isinstance(self.phases, Unset):
            phases = self.phases



        angle = self.angle

        rotation = self.rotation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
        })
        if target is not UNSET:
            field_dict["target"] = target
        if targets is not UNSET:
            field_dict["targets"] = targets
        if controls is not UNSET:
            field_dict["controls"] = controls
        if phase is not UNSET:
            field_dict["phase"] = phase
        if phases is not UNSET:
            field_dict["phases"] = phases
        if angle is not UNSET:
            field_dict["angle"] = angle
        if rotation is not UNSET:
            field_dict["rotation"] = rotation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_native_gate(d.pop("gate"))




        target = d.pop("target", UNSET)

        targets = cast(list[float], d.pop("targets", UNSET))


        controls = cast(list[float], d.pop("controls", UNSET))


        phase = d.pop("phase", UNSET)

        phases = cast(list[float], d.pop("phases", UNSET))


        angle = d.pop("angle", UNSET)

        rotation = d.pop("rotation", UNSET)

        gate_native_gate = cls(
            gate=gate,
            target=target,
            targets=targets,
            controls=controls,
            phase=phase,
            phases=phases,
            angle=angle,
            rotation=rotation,
        )

        return gate_native_gate
