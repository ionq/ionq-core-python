# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="Backend")



@_attrs_define
class Backend:
    """ A backend that you can target your program to run on.

        Attributes:
            average_queue_time (float): Current wait time on the queue for execution. Example: 1181215.
            backend (str): Specifies target hardware and generation where applies: `simulator`, `qpu.aria-1`, `qpu.aria-2`,
                `qpu.forte-1`, `qpu.forte-enterprise-1`, `qpu.forte-enterprise-2`, `qpu.forte-enterprise-3` Example: qpu.aria-1.
            last_updated (str): Last date time the backend status was updated. Example: 2025-06-16T00:00:00Z.
            qubits (int): The number of qubits available. Example: 25.
            status (str): Current status of the backend: `available`, `unavailable`, `retired`.
            characterization_id (str | Unset): Current characterization ID for this backend Example:
                617a1f8b-59d4-435d-aa33-695433d7155e.
            degraded (bool | Unset): Flag to tell if the backend is degraded or not.
            kw (float | Unset): The amount of energy used by the backend in kilowatt-hours. Example: 4902.81.
            location (str | Unset): The location of the backend. Example: College Park, MD, USA.
     """

    average_queue_time: float
    backend: str
    last_updated: str
    qubits: int
    status: str
    characterization_id: str | Unset = UNSET
    degraded: bool | Unset = UNSET
    kw: float | Unset = UNSET
    location: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        average_queue_time = self.average_queue_time

        backend = self.backend

        last_updated = self.last_updated

        qubits = self.qubits

        status = self.status

        characterization_id = self.characterization_id

        degraded = self.degraded

        kw = self.kw

        location = self.location


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "average_queue_time": average_queue_time,
            "backend": backend,
            "last_updated": last_updated,
            "qubits": qubits,
            "status": status,
        })
        if characterization_id is not UNSET:
            field_dict["characterization_id"] = characterization_id
        if degraded is not UNSET:
            field_dict["degraded"] = degraded
        if kw is not UNSET:
            field_dict["kw"] = kw
        if location is not UNSET:
            field_dict["location"] = location

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        average_queue_time = d.pop("average_queue_time")

        backend = d.pop("backend")

        last_updated = d.pop("last_updated")

        qubits = d.pop("qubits")

        status = d.pop("status")

        characterization_id = d.pop("characterization_id", UNSET)

        degraded = d.pop("degraded", UNSET)

        kw = d.pop("kw", UNSET)

        location = d.pop("location", UNSET)

        backend = cls(
            average_queue_time=average_queue_time,
            backend=backend,
            last_updated=last_updated,
            qubits=qubits,
            status=status,
            characterization_id=characterization_id,
            degraded=degraded,
            kw=kw,
            location=location,
        )


        backend.additional_properties = d
        return backend

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
