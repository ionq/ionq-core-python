# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gate_swap_gate import check_gate_swap_gate
from ..models.gate_swap_gate import GateSwapGate
from typing import cast






T = TypeVar("T", bound="GateSwap")



@_attrs_define
class GateSwap:
    """ Two-qubit SWAP.

        Attributes:
            gate (GateSwapGate):
            targets (list[int]): The two qubits the gate acts on.
     """

    gate: GateSwapGate
    targets: list[int]





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets = self.targets




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
            "targets": targets,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_gate_swap_gate(d.pop("gate"))




        targets = cast(list[int], d.pop("targets"))


        gate_swap = cls(
            gate=gate,
            targets=targets,
        )

        return gate_swap

