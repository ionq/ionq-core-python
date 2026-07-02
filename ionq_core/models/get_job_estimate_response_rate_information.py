# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_job_estimate_response_rate_information_rate_type import check_get_job_estimate_response_rate_information_rate_type
from ..models.get_job_estimate_response_rate_information_rate_type import GetJobEstimateResponseRateInformationRateType
from typing import cast






T = TypeVar("T", bound="GetJobEstimateResponseRateInformation")



@_attrs_define
class GetJobEstimateResponseRateInformation:
    """ 
        Attributes:
            qct_cost_cents (float | None):
            rate_type (GetJobEstimateResponseRateInformationRateType):
            job_cost_minimum (float | None):
            cost_2q_gate (float | None):
            cost_1q_gate (float | None):
            organization (str):
     """

    qct_cost_cents: float | None
    rate_type: GetJobEstimateResponseRateInformationRateType
    job_cost_minimum: float | None
    cost_2q_gate: float | None
    cost_1q_gate: float | None
    organization: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        qct_cost_cents: float | None
        qct_cost_cents = self.qct_cost_cents

        rate_type: str = self.rate_type

        job_cost_minimum: float | None
        job_cost_minimum = self.job_cost_minimum

        cost_2q_gate: float | None
        cost_2q_gate = self.cost_2q_gate

        cost_1q_gate: float | None
        cost_1q_gate = self.cost_1q_gate

        organization = self.organization


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "qct_cost_cents": qct_cost_cents,
            "rate_type": rate_type,
            "job_cost_minimum": job_cost_minimum,
            "cost_2q_gate": cost_2q_gate,
            "cost_1q_gate": cost_1q_gate,
            "organization": organization,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_qct_cost_cents(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        qct_cost_cents = _parse_qct_cost_cents(d.pop("qct_cost_cents"))


        rate_type = check_get_job_estimate_response_rate_information_rate_type(d.pop("rate_type"))




        def _parse_job_cost_minimum(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        job_cost_minimum = _parse_job_cost_minimum(d.pop("job_cost_minimum"))


        def _parse_cost_2q_gate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        cost_2q_gate = _parse_cost_2q_gate(d.pop("cost_2q_gate"))


        def _parse_cost_1q_gate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        cost_1q_gate = _parse_cost_1q_gate(d.pop("cost_1q_gate"))


        organization = d.pop("organization")

        get_job_estimate_response_rate_information = cls(
            qct_cost_cents=qct_cost_cents,
            rate_type=rate_type,
            job_cost_minimum=job_cost_minimum,
            cost_2q_gate=cost_2q_gate,
            cost_1q_gate=cost_1q_gate,
            organization=organization,
        )


        get_job_estimate_response_rate_information.additional_properties = d
        return get_job_estimate_response_rate_information

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
