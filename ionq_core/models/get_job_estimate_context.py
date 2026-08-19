# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GetJobEstimateContext")



@_attrs_define
class GetJobEstimateContext:
    """
        Attributes:
            backend (str): Available options: `simulator`, `qpu.forte-1`, `qpu.forte-enterprise-1`
            organization (None | str):
            project (None | str):
            type_ (str | Unset):  Default: 'ionq.circuit.v1'.
            qubits (int | Unset):  Default: 25.
            shots (int | Unset):  Default: 1000.
            field_1q_gates (int | Unset):  Default: 0.
            field_2q_gates (int | Unset):  Default: 0.
            error_mitigation (bool | Unset):  Default: False.
     """

    backend: str
    organization: None | str
    project: None | str
    type_: str | Unset = 'ionq.circuit.v1'
    qubits: int | Unset = 25
    shots: int | Unset = 1000
    field_1q_gates: int | Unset = 0
    field_2q_gates: int | Unset = 0
    error_mitigation: bool | Unset = False





    def to_dict(self) -> dict[str, Any]:
        backend = self.backend

        organization: None | str
        organization = self.organization

        project: None | str
        project = self.project

        type_ = self.type_

        qubits = self.qubits

        shots = self.shots

        field_1q_gates = self.field_1q_gates

        field_2q_gates = self.field_2q_gates

        error_mitigation = self.error_mitigation


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "backend": backend,
            "organization": organization,
            "project": project,
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if qubits is not UNSET:
            field_dict["qubits"] = qubits
        if shots is not UNSET:
            field_dict["shots"] = shots
        if field_1q_gates is not UNSET:
            field_dict["1q_gates"] = field_1q_gates
        if field_2q_gates is not UNSET:
            field_dict["2q_gates"] = field_2q_gates
        if error_mitigation is not UNSET:
            field_dict["error_mitigation"] = error_mitigation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend = d.pop("backend")

        def _parse_organization(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization = _parse_organization(d.pop("organization"))


        def _parse_project(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        project = _parse_project(d.pop("project"))


        type_ = d.pop("type", UNSET)

        qubits = d.pop("qubits", UNSET)

        shots = d.pop("shots", UNSET)

        field_1q_gates = d.pop("1q_gates", UNSET)

        field_2q_gates = d.pop("2q_gates", UNSET)

        error_mitigation = d.pop("error_mitigation", UNSET)

        get_job_estimate_context = cls(
            backend=backend,
            organization=organization,
            project=project,
            type_=type_,
            qubits=qubits,
            shots=shots,
            field_1q_gates=field_1q_gates,
            field_2q_gates=field_2q_gates,
            error_mitigation=error_mitigation,
        )

        return get_job_estimate_context
