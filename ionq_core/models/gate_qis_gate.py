from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qis_gate import check_qis_gate
from ..models.qis_gate import QisGate
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GateQisGate")



@_attrs_define
class GateQisGate:
    """ 
        Attributes:
            gate (QisGate):
            targets (list[float] | Unset): The qubits that a quantum gate is applied to
            controls (list[float] | Unset): The qubits that determine whether the operation is applied to targets.
            target (int | Unset): Single qubit target (alternative to targets array)
            control (int | Unset): Single control qubit (alternative to controls array)
            rotation (float | Unset): Rotation angle for rx/ry/rz gates
     """

    gate: QisGate
    targets: list[float] | Unset = UNSET
    controls: list[float] | Unset = UNSET
    target: int | Unset = UNSET
    control: int | Unset = UNSET
    rotation: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets: list[float] | Unset = UNSET
        if not isinstance(self.targets, Unset):
            targets = self.targets



        controls: list[float] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls



        target = self.target

        control = self.control

        rotation = self.rotation


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
        if control is not UNSET:
            field_dict["control"] = control
        if rotation is not UNSET:
            field_dict["rotation"] = rotation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_qis_gate(d.pop("gate"))




        targets = cast(list[float], d.pop("targets", UNSET))


        controls = cast(list[float], d.pop("controls", UNSET))


        target = d.pop("target", UNSET)

        control = d.pop("control", UNSET)

        rotation = d.pop("rotation", UNSET)

        gate_qis_gate = cls(
            gate=gate,
            targets=targets,
            controls=controls,
            target=target,
            control=control,
            rotation=rotation,
        )

        return gate_qis_gate

