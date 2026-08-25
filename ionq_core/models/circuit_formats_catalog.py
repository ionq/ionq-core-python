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
  from ..models.ionq_native_v1 import IonqNativeV1





T = TypeVar("T", bound="CircuitFormatsCatalog")



@_attrs_define
class CircuitFormatsCatalog:
    """ Catalog of supported circuit artifact formats. The same identifiers are used
    both when a circuit is submitted (the job `input` payload) and when the
    compiler emits a transpiled circuit (the job `output.compilation.compiled_circuits`
    map) — both are circuits, just at different stages of the pipeline.

    Each property below documents one format's payload structure. Used by the
    Circuit formats docs page.

        Attributes:
            ionq_native_v1 (IonqNativeV1): `ionq.native.v1` — Compiled circuit expressed in IonQ native gates.
                Same shape as the native-gate circuit accepted on job creation:
                a qubit count plus an ordered list of native gate operations. Example: {'qubits': 2, 'circuit': [{'gate': 'ms',
                'targets': [0, 1], 'phases': [0, 0.25]}, {'gate': 'gpi2', 'target': 0, 'phase': 0.75}]}.
            ionq_qasm3_v1 (str): `ionq.qasm3.v1` — Circuit expressed as an OpenQASM 3 program.
                On submission the program is the job's `input.data`; when the compiler
                emits this format the artifact payload is the program source itself —
                download it with the descriptor's `id` and read its `media_type` for the
                content type.
                IonQ accepts a subset of the language — see the
                [OpenQASM 3](/api-reference/v0.4/openqasm3) page for the supported constructs. Example: OPENQASM 3.0;
                qubit[2] q;
                bit[2] c;
                h q[0];
                cx q[0], q[1];
                c[0] = measure q[0];
                c[1] = measure q[1];.
     """

    ionq_native_v1: IonqNativeV1
    ionq_qasm3_v1: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.ionq_native_v1 import IonqNativeV1
        ionq_native_v1 = self.ionq_native_v1.to_dict()

        ionq_qasm3_v1 = self.ionq_qasm3_v1


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ionq.native.v1": ionq_native_v1,
            "ionq.qasm3.v1": ionq_qasm3_v1,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ionq_native_v1 import IonqNativeV1
        d = dict(src_dict)
        ionq_native_v1 = IonqNativeV1.from_dict(d.pop("ionq.native.v1"))




        ionq_qasm3_v1 = d.pop("ionq.qasm3.v1")

        circuit_formats_catalog = cls(
            ionq_native_v1=ionq_native_v1,
            ionq_qasm3_v1=ionq_qasm3_v1,
        )

        return circuit_formats_catalog
