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
  from ..models.registered_histogram_registers import RegisteredHistogramRegisters





T = TypeVar("T", bound="RegisteredHistogram")



@_attrs_define
class RegisteredHistogram:
    """ Per-register histogram counts.

        Attributes:
            registers (RegisteredHistogramRegisters): Per-register shot counts, keyed by register name.
     """

    registers: RegisteredHistogramRegisters





    def to_dict(self) -> dict[str, Any]:
        from ..models.registered_histogram_registers import RegisteredHistogramRegisters
        registers = self.registers.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "registers": registers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registered_histogram_registers import RegisteredHistogramRegisters
        d = dict(src_dict)
        registers = RegisteredHistogramRegisters.from_dict(d.pop("registers"))




        registered_histogram = cls(
            registers=registers,
        )

        return registered_histogram
