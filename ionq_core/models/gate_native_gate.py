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
            type_ (NativeGate):
            targets (list[float]): The qubits that a quantum gate is applied to
            controls (list[float] | Unset): The qubits that determine whether the operation is applied to targets.
     """

    type_: NativeGate
    targets: list[float]
    controls: list[float] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        targets = self.targets



        controls: list[float] | Unset = UNSET
        if not isinstance(self.controls, Unset):
            controls = self.controls




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "targets": targets,
        })
        if controls is not UNSET:
            field_dict["controls"] = controls

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_native_gate(d.pop("type"))




        targets = cast(list[float], d.pop("targets"))


        controls = cast(list[float], d.pop("controls", UNSET))


        gate_native_gate = cls(
            type_=type_,
            targets=targets,
            controls=controls,
        )

        return gate_native_gate

