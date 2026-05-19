# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gate_pauliexp_gate import check_gate_pauliexp_gate
from ..models.gate_pauliexp_gate import GatePauliexpGate
from typing import cast






T = TypeVar("T", bound="GatePauliexp")



@_attrs_define
class GatePauliexp:
    """ Sparse Pauli exponential gate. Trotter-decomposed per term:

      U = prod_k exp(-i * coefficients[k] * time * P_k)

    where P_k is the tensor product of single-qubit Paulis encoded
    as `terms[k]`, and `terms[k][i]` (a character in {I,X,Y,Z}) acts
    on the qubit at `targets[i]`.

    `time` is a global multiplier on every coefficient.

    Constraints:
      * `terms[k]` has length equal to `len(targets)` for every k.
      * `coefficients` has the same length as `terms`.
      * `coefficients` are real numbers.
      * `time` is strictly positive.
      * Endianness: `terms[k][0]` acts on `targets[0]` (big-endian
        by position).

    Because the formula is a Trotter decomposition, non-commuting
    terms yield an approximation rather than the exact exp(-i t H).

        Attributes:
            gate (GatePauliexpGate):
            targets (list[int]): Qubits the Pauli operators act on, in order.
            terms (list[str]): Pauli words in {I, X, Y, Z}. `terms[k][i]` acts on
                `targets[i]`. Every term has length equal to `len(targets)`.
            coefficients (list[float]): Real coefficient for each Pauli term, parallel to `terms`.
            time (float): Strictly-positive global multiplier. The kth term's
                effective rotation is `coefficients[k] * time`.
     """

    gate: GatePauliexpGate
    targets: list[int]
    terms: list[str]
    coefficients: list[float]
    time: float





    def to_dict(self) -> dict[str, Any]:
        gate: str = self.gate

        targets = self.targets



        terms = self.terms



        coefficients = self.coefficients



        time = self.time


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gate": gate,
            "targets": targets,
            "terms": terms,
            "coefficients": coefficients,
            "time": time,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gate = check_gate_pauliexp_gate(d.pop("gate"))




        targets = cast(list[int], d.pop("targets"))


        terms = cast(list[str], d.pop("terms"))


        coefficients = cast(list[float], d.pop("coefficients"))


        time = d.pop("time")

        gate_pauliexp = cls(
            gate=gate,
            targets=targets,
            terms=terms,
            coefficients=coefficients,
            time=time,
        )

        return gate_pauliexp

