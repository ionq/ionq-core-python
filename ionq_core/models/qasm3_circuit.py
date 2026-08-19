# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="QASM3Circuit")



@_attrs_define
class QASM3Circuit:
    r""" Submit an OpenQASM 3 program with `type: ionq.qasm3.v1`. `data` carries the program source as a single string. IonQ
    accepts a subset of the language — see the [OpenQASM 3](/api-reference/v0.4/openqasm3) page.

        Example:
            {'data': 'OPENQASM 3.0;\ninclude "stdgates.inc";\nqubit[2] q;\nbit[2] c;\nh q[0];\ncx q[0], q[1];\nc[0] =
                measure q[0];\nc[1] = measure q[1];\n'}

        Attributes:
            data (str): The OpenQASM 3 program to run, as a single string.
     """

    data: str





    def to_dict(self) -> dict[str, Any]:
        data = self.data


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = d.pop("data")

        qasm3_circuit = cls(
            data=data,
        )

        return qasm3_circuit

