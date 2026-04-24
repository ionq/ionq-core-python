# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.native_circuit_gateset import check_native_circuit_gateset
from ..models.native_circuit_gateset import NativeCircuitGateset
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.gate_native_gate import GateNativeGate
  from ..models.registers import Registers





T = TypeVar("T", bound="NativeCircuit")



@_attrs_define
class NativeCircuit:
    """ 
        Attributes:
            circuit (list[GateNativeGate]): Circuit gates. Can be either QIS gates or Native gates depending on the gateset
                property.
            name (str | Unset):
            qubits (int | Unset):
            registers (Registers | Unset):
            gateset (NativeCircuitGateset | Unset): Optional gateset override for this individual circuit. If not specified,
                inherits from parent.
                When set, the circuit must use the appropriate gate format (Native).
     """

    circuit: list[GateNativeGate]
    name: str | Unset = UNSET
    qubits: int | Unset = UNSET
    registers: Registers | Unset = UNSET
    gateset: NativeCircuitGateset | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.gate_native_gate import GateNativeGate
        from ..models.registers import Registers
        circuit = []
        for circuit_item_data in self.circuit:
            circuit_item = circuit_item_data.to_dict()
            circuit.append(circuit_item)



        name = self.name

        qubits = self.qubits

        registers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.registers, Unset):
            registers = self.registers.to_dict()

        gateset: str | Unset = UNSET
        if not isinstance(self.gateset, Unset):
            gateset = self.gateset



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "circuit": circuit,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if qubits is not UNSET:
            field_dict["qubits"] = qubits
        if registers is not UNSET:
            field_dict["registers"] = registers
        if gateset is not UNSET:
            field_dict["gateset"] = gateset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gate_native_gate import GateNativeGate
        from ..models.registers import Registers
        d = dict(src_dict)
        circuit = []
        _circuit = d.pop("circuit")
        for circuit_item_data in (_circuit):
            circuit_item = GateNativeGate.from_dict(circuit_item_data)



            circuit.append(circuit_item)


        name = d.pop("name", UNSET)

        qubits = d.pop("qubits", UNSET)

        _registers = d.pop("registers", UNSET)
        registers: Registers | Unset
        if isinstance(_registers,  Unset):
            registers = UNSET
        else:
            registers = Registers.from_dict(_registers)




        _gateset = d.pop("gateset", UNSET)
        gateset: NativeCircuitGateset | Unset
        if isinstance(_gateset,  Unset):
            gateset = UNSET
        else:
            gateset = check_native_circuit_gateset(_gateset)




        native_circuit = cls(
            circuit=circuit,
            name=name,
            qubits=qubits,
            registers=registers,
            gateset=gateset,
        )

        return native_circuit

