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
            targets (list[float] | Unset): The qubits that a quantum gate is applied to
            controls (list[float] | Unset): The qubits that determine whether the operation is applied to targets.
            target (int | Unset): Single qubit target (alternative to targets array)
            phase (float | Unset): Phase for gpi/gpi2 gates
            phases (list[float] | Unset): Phases for ms gate
            angle (float | Unset): Interaction angle for ms gate (in turns, default 0.25)
     """

    gate: NativeGate
    targets: list[float] | Unset = UNSET
    controls: list[float] | Unset = UNSET
    target: int | Unset = UNSET
    phase: float | Unset = UNSET
    phases: list[float] | Unset = UNSET
    angle: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets: list[float] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = self.targets



        controls: list[float] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls



        target = self.target

        phase = self.phase

        phases: list[float] | Unset = UNSET
        if not isinstance(self.phases, Unset):
            phases = self.phases



        angle = self.angle


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
        })
        if targets is not UNSET:
            field_dict["targets"] = targets
        if controls is not UNSET:
            field_dict["controls"] = controls
        if target is not UNSET:
            field_dict["target"] = target
        if phase is not UNSET:
            field_dict["phase"] = phase
        if phases is not UNSET:
            field_dict["phases"] = phases
        if angle is not UNSET:
            field_dict["angle"] = angle

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_native_gate(d.pop("gate"))




        targets = cast(list[float], d.pop("targets", UNSET))


        controls = cast(list[float], d.pop("controls", UNSET))


        target = d.pop("target", UNSET)

        phase = d.pop("phase", UNSET)

        phases = cast(list[float], d.pop("phases", UNSET))


        angle = d.pop("angle", UNSET)

        gate_native_gate = cls(
            gate=gate,
            targets=targets,
            controls=controls,
            target=target,
            phase=phase,
            phases=phases,
            angle=angle,
        )

        return gate_native_gate

