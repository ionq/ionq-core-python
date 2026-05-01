# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qis_circuit_input_gateset import check_qis_circuit_input_gateset
from ..models.qis_circuit_input_gateset import QisCircuitInputGateset
from typing import cast

if TYPE_CHECKING:
  from ..models.gate_qis_gate import GateQisGate





T = TypeVar("T", bound="QisCircuitInput")



@_attrs_define
class QisCircuitInput:
    """ 
        Attributes:
            qubits (int):
            circuit (list[GateQisGate]):
            gateset (QisCircuitInputGateset):
     """

    qubits: int
    circuit: list[GateQisGate]
    gateset: QisCircuitInputGateset





    def to_dict(self) -> dict[str, Any]:
        from ..models.gate_qis_gate import GateQisGate
        qubits = self.qubits

        circuit = []
        for circuit_item_data in self.circuit:
            circuit_item = circuit_item_data.to_dict()
            circuit.append(circuit_item)



        gateset: str = self.gateset


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "qubits": qubits,
            "circuit": circuit,
            "gateset": gateset,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gate_qis_gate import GateQisGate
        d = dict(src_dict)
        qubits = d.pop("qubits")

        circuit = []
        _circuit = d.pop("circuit")
        for circuit_item_data in (_circuit):
            circuit_item = GateQisGate.from_dict(circuit_item_data)



            circuit.append(circuit_item)


        gateset = check_qis_circuit_input_gateset(d.pop("gateset"))




        qis_circuit_input = cls(
            qubits=qubits,
            circuit=circuit,
            gateset=gateset,
        )

        return qis_circuit_input

