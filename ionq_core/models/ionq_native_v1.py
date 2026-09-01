# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.gate_native_gate import GateNativeGate





T = TypeVar("T", bound="IonqNativeV1")



@_attrs_define
class IonqNativeV1:
    """ `ionq.native.v1` — Compiled circuit expressed in IonQ native gates.
    Same shape as the native-gate circuit accepted on job creation:
    a qubit count plus an ordered list of native gate operations.

        Example:
            {'qubits': 2, 'circuit': [{'gate': 'ms', 'targets': [0, 1], 'phases': [0, 0.25]}, {'gate': 'gpi2', 'target': 0,
                'phase': 0.75}]}

        Attributes:
            qubits (int): Number of qubits used by the compiled circuit.
            circuit (list[GateNativeGate]): Ordered list of native gate operations.
     """

    qubits: int
    circuit: list[GateNativeGate]





    def to_dict(self) -> dict[str, Any]:
        from ..models.gate_native_gate import GateNativeGate
        qubits = self.qubits

        circuit = []
        for circuit_item_data in self.circuit:
            circuit_item = circuit_item_data.to_dict()
            circuit.append(circuit_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "qubits": qubits,
            "circuit": circuit,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gate_native_gate import GateNativeGate
        d = dict(src_dict)
        qubits = d.pop("qubits")

        circuit = []
        _circuit = d.pop("circuit")
        for circuit_item_data in (_circuit):
            circuit_item = GateNativeGate.from_dict(circuit_item_data)



            circuit.append(circuit_item)


        ionq_native_v1 = cls(
            qubits=qubits,
            circuit=circuit,
        )

        return ionq_native_v1

