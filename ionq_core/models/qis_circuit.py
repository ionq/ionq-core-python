# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qis_circuit_gateset import check_qis_circuit_gateset
from ..models.qis_circuit_gateset import QISCircuitGateset
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.gate_cnot import GateCnot
  from ..models.gate_h import GateH
  from ..models.gate_not import GateNot
  from ..models.gate_pauliexp import GatePauliexp
  from ..models.gate_rx import GateRx
  from ..models.gate_ry import GateRy
  from ..models.gate_rz import GateRz
  from ..models.gate_s import GateS
  from ..models.gate_si import GateSi
  from ..models.gate_swap import GateSwap
  from ..models.gate_t import GateT
  from ..models.gate_ti import GateTi
  from ..models.gate_v import GateV
  from ..models.gate_vi import GateVi
  from ..models.gate_x import GateX
  from ..models.gate_xx import GateXX
  from ..models.gate_y import GateY
  from ..models.gate_yy import GateYY
  from ..models.gate_z import GateZ
  from ..models.gate_zz import GateZZ
  from ..models.registers import Registers





T = TypeVar("T", bound="QISCircuit")



@_attrs_define
class QISCircuit:
    """ 
        Attributes:
            circuit (list[GateCnot | GateH | GateNot | GatePauliexp | GateRx | GateRy | GateRz | GateS | GateSi | GateSwap |
                GateT | GateTi | GateV | GateVi | GateX | GateXX | GateY | GateYY | GateZ | GateZZ]): Circuit gates. Can be
                either QIS gates or Native gates depending on the gateset property.
            name (str | Unset):
            qubits (int | Unset):
            registers (Registers | Unset):
            gateset (QISCircuitGateset | Unset): Optional gateset override for this individual circuit. If not specified,
                inherits from parent.
                When set, the circuit must use the appropriate gate format (QIS).
     """

    circuit: list[GateCnot | GateH | GateNot | GatePauliexp | GateRx | GateRy | GateRz | GateS | GateSi | GateSwap | GateT | GateTi | GateV | GateVi | GateX | GateXX | GateY | GateYY | GateZ | GateZZ]
    name: str | Unset = UNSET
    qubits: int | Unset = UNSET
    registers: Registers | Unset = UNSET
    gateset: QISCircuitGateset | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.gate_cnot import GateCnot
        from ..models.gate_h import GateH
        from ..models.gate_not import GateNot
        from ..models.gate_pauliexp import GatePauliexp
        from ..models.gate_rx import GateRx
        from ..models.gate_ry import GateRy
        from ..models.gate_rz import GateRz
        from ..models.gate_s import GateS
        from ..models.gate_si import GateSi
        from ..models.gate_swap import GateSwap
        from ..models.gate_t import GateT
        from ..models.gate_ti import GateTi
        from ..models.gate_v import GateV
        from ..models.gate_vi import GateVi
        from ..models.gate_x import GateX
        from ..models.gate_xx import GateXX
        from ..models.gate_y import GateY
        from ..models.gate_yy import GateYY
        from ..models.gate_z import GateZ
        from ..models.gate_zz import GateZZ
        from ..models.registers import Registers
        circuit = []
        for circuit_item_data in self.circuit:
            circuit_item: dict[str, Any]
            if isinstance(circuit_item_data, GatePauliexp):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateCnot):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateSwap):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateRx):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateRy):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateRz):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateXX):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateYY):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateZZ):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateNot):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateX):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateY):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateZ):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateH):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateS):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateSi):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateT):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateTi):
                circuit_item = circuit_item_data.to_dict()
            elif isinstance(circuit_item_data, GateV):
                circuit_item = circuit_item_data.to_dict()
            else:
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
        from ..models.gate_cnot import GateCnot
        from ..models.gate_h import GateH
        from ..models.gate_not import GateNot
        from ..models.gate_pauliexp import GatePauliexp
        from ..models.gate_rx import GateRx
        from ..models.gate_ry import GateRy
        from ..models.gate_rz import GateRz
        from ..models.gate_s import GateS
        from ..models.gate_si import GateSi
        from ..models.gate_swap import GateSwap
        from ..models.gate_t import GateT
        from ..models.gate_ti import GateTi
        from ..models.gate_v import GateV
        from ..models.gate_vi import GateVi
        from ..models.gate_x import GateX
        from ..models.gate_xx import GateXX
        from ..models.gate_y import GateY
        from ..models.gate_yy import GateYY
        from ..models.gate_z import GateZ
        from ..models.gate_zz import GateZZ
        from ..models.registers import Registers
        d = dict(src_dict)
        circuit = []
        _circuit = d.pop("circuit")
        for circuit_item_data in (_circuit):
            def _parse_circuit_item(data: object) -> GateCnot | GateH | GateNot | GatePauliexp | GateRx | GateRy | GateRz | GateS | GateSi | GateSwap | GateT | GateTi | GateV | GateVi | GateX | GateXX | GateY | GateYY | GateZ | GateZZ:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_0 = GatePauliexp.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_1 = GateCnot.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_2 = GateSwap.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_3 = GateRx.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_4 = GateRy.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_5 = GateRz.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_6 = GateXX.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_6
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_7 = GateYY.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_7
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_8 = GateZZ.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_8
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_9 = GateNot.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_9
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_10 = GateX.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_10
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_11 = GateY.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_11
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_12 = GateZ.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_12
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_13 = GateH.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_13
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_14 = GateS.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_14
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_15 = GateSi.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_15
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_16 = GateT.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_16
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_17 = GateTi.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_17
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_gate_qis_gate_type_18 = GateV.from_dict(data)



                    return componentsschemas_gate_qis_gate_type_18
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_gate_qis_gate_type_19 = GateVi.from_dict(data)



                return componentsschemas_gate_qis_gate_type_19

            circuit_item = _parse_circuit_item(circuit_item_data)

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
        gateset: QISCircuitGateset | Unset
        if isinstance(_gateset,  Unset):
            gateset = UNSET
        else:
            gateset = check_qis_circuit_gateset(_gateset)




        qis_circuit = cls(
            circuit=circuit,
            name=name,
            qubits=qubits,
            registers=registers,
            gateset=gateset,
        )

        return qis_circuit

