# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CircuitJobSettingsErrorMitigationDebiasingType0PhiChiTwirling")



@_attrs_define
class CircuitJobSettingsErrorMitigationDebiasingType0PhiChiTwirling:
    """ 
        Attributes:
            p2q (float | Unset):
            t2q (float | Unset):
            t1q (float | Unset):
     """

    p2q: float | Unset = UNSET
    t2q: float | Unset = UNSET
    t1q: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        p2q = self.p2q

        t2q = self.t2q

        t1q = self.t1q


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if p2q is not UNSET:
            field_dict["p2q"] = p2q
        if t2q is not UNSET:
            field_dict["t2q"] = t2q
        if t1q is not UNSET:
            field_dict["t1q"] = t1q

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        p2q = d.pop("p2q", UNSET)

        t2q = d.pop("t2q", UNSET)

        t1q = d.pop("t1q", UNSET)

        circuit_job_settings_error_mitigation_debiasing_type_0_phi_chi_twirling = cls(
            p2q=p2q,
            t2q=t2q,
            t1q=t1q,
        )


        circuit_job_settings_error_mitigation_debiasing_type_0_phi_chi_twirling.additional_properties = d
        return circuit_job_settings_error_mitigation_debiasing_type_0_phi_chi_twirling

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
