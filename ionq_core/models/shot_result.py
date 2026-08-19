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
  from ..models.shot_registers import ShotRegisters





T = TypeVar("T", bound="ShotResult")



@_attrs_define
class ShotResult:
    """ Result of a single shot — measured bit arrays for every named register.

        Attributes:
            registers (ShotRegisters): Per-register bit arrays for one shot, keyed by register name.
     """

    registers: ShotRegisters





    def to_dict(self) -> dict[str, Any]:
        from ..models.shot_registers import ShotRegisters
        registers = self.registers.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "registers": registers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shot_registers import ShotRegisters
        d = dict(src_dict)
        registers = ShotRegisters.from_dict(d.pop("registers"))




        shot_result = cls(
            registers=registers,
        )

        return shot_result

