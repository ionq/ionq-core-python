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
            targets (list[float]): The qubits that a quantum gate is applied to
            gate (NativeGate):
            controls (list[float] | Unset): The qubits that determine whether the operation is applied to targets.
     """

    targets: list[float]
    gate: NativeGate
    controls: list[float] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        targets = self.targets



        gate: str = self.gate

        controls: list[float] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "targets": targets,
            "gate": gate,
        })
        if controls is not UNSET:
            field_dict["controls"] = controls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        targets = cast(list[float], d.pop("targets"))


        gate = check_native_gate(d.pop("gate"))




        controls = cast(list[float], d.pop("controls", UNSET))


        gate_native_gate = cls(
            targets=targets,
            gate=gate,
            controls=controls,
        )

        return gate_native_gate

