# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gate_zz_gate import check_gate_zz_gate
from ..models.gate_zz_gate import GateZZGate
from typing import cast






T = TypeVar("T", bound="GateZZ")



@_attrs_define
class GateZZ:
    """ Two-qubit ZZ (Ising-ZZ) rotation, exp(-i theta/2 Z⊗Z), with
    `rotation` in radians. Distinct from the native-gateset `zz`,
    which takes a `phase` parameter in turns.

        Attributes:
            gate (GateZZGate):
            targets (list[int]): The two qubits the gate acts on.
            rotation (float): Rotation angle in radians.
     """

    gate: GateZZGate
    targets: list[int]
    rotation: float





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets = self.targets



        rotation = self.rotation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
            "targets": targets,
            "rotation": rotation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_gate_zz_gate(d.pop("gate"))




        targets = cast(list[int], d.pop("targets"))


        rotation = d.pop("rotation")

        gate_zz = cls(
            gate=gate,
            targets=targets,
            rotation=rotation,
        )

        return gate_zz

