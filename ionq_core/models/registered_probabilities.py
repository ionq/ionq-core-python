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
  from ..models.registered_probabilities_registers import RegisteredProbabilitiesRegisters





T = TypeVar("T", bound="RegisteredProbabilities")



@_attrs_define
class RegisteredProbabilities:
    """ Per-register probability distributions, keyed by register name.

        Attributes:
            registers (RegisteredProbabilitiesRegisters): Bitstring → probability map for this register.
     """

    registers: RegisteredProbabilitiesRegisters





    def to_dict(self) -> dict[str, Any]:
        from ..models.registered_probabilities_registers import RegisteredProbabilitiesRegisters
        registers = self.registers.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "registers": registers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registered_probabilities_registers import RegisteredProbabilitiesRegisters
        d = dict(src_dict)
        registers = RegisteredProbabilitiesRegisters.from_dict(d.pop("registers"))




        registered_probabilities = cls(
            registers=registers,
        )

        return registered_probabilities
