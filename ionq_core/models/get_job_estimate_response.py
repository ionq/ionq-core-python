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

if TYPE_CHECKING:
  from ..models.get_job_estimate_context import GetJobEstimateContext
  from ..models.get_job_estimate_response_rate_card import GetJobEstimateResponseRateCard





T = TypeVar("T", bound="GetJobEstimateResponse")



@_attrs_define
class GetJobEstimateResponse:
    """
        Attributes:
            estimate_context (GetJobEstimateContext):
            estimated_at (str):
            estimated_unit (str):
            rate_card (GetJobEstimateResponseRateCard):
            estimated_total_cost (float):
            estimated_execution_time (int): Predicted job execution time, in milliseconds. Example: 96250.
            current_predicted_queue_time (int): Predicted time this job will wait in the queue before running, in
                milliseconds. Example: 397577.
            estimated_quantum_compute_time_us (int | Unset): Predicted quantum compute time, in microseconds. Only present
                for
                compute_second priced backends.
     """

    estimate_context: GetJobEstimateContext
    estimated_at: str
    estimated_unit: str
    rate_card: GetJobEstimateResponseRateCard
    estimated_total_cost: float
    estimated_execution_time: int
    current_predicted_queue_time: int
    estimated_quantum_compute_time_us: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_job_estimate_context import GetJobEstimateContext
        from ..models.get_job_estimate_response_rate_card import GetJobEstimateResponseRateCard
        estimate_context = self.estimate_context.to_dict()

        estimated_at = self.estimated_at

        estimated_unit = self.estimated_unit

        rate_card = self.rate_card.to_dict()

        estimated_total_cost = self.estimated_total_cost

        estimated_execution_time = self.estimated_execution_time

        current_predicted_queue_time = self.current_predicted_queue_time

        estimated_quantum_compute_time_us = self.estimated_quantum_compute_time_us


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "estimate_context": estimate_context,
            "estimated_at": estimated_at,
            "estimated_unit": estimated_unit,
            "rate_card": rate_card,
            "estimated_total_cost": estimated_total_cost,
            "estimated_execution_time": estimated_execution_time,
            "current_predicted_queue_time": current_predicted_queue_time,
        })
        if estimated_quantum_compute_time_us is not UNSET:
            field_dict["estimated_quantum_compute_time_us"] = estimated_quantum_compute_time_us

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_job_estimate_context import GetJobEstimateContext
        from ..models.get_job_estimate_response_rate_card import GetJobEstimateResponseRateCard
        d = dict(src_dict)
        estimate_context = GetJobEstimateContext.from_dict(d.pop("estimate_context"))




        estimated_at = d.pop("estimated_at")

        estimated_unit = d.pop("estimated_unit")

        rate_card = GetJobEstimateResponseRateCard.from_dict(d.pop("rate_card"))




        estimated_total_cost = d.pop("estimated_total_cost")

        estimated_execution_time = d.pop("estimated_execution_time")

        current_predicted_queue_time = d.pop("current_predicted_queue_time")

        estimated_quantum_compute_time_us = d.pop("estimated_quantum_compute_time_us", UNSET)

        get_job_estimate_response = cls(
            estimate_context=estimate_context,
            estimated_at=estimated_at,
            estimated_unit=estimated_unit,
            rate_card=rate_card,
            estimated_total_cost=estimated_total_cost,
            estimated_execution_time=estimated_execution_time,
            current_predicted_queue_time=current_predicted_queue_time,
            estimated_quantum_compute_time_us=estimated_quantum_compute_time_us,
        )

        return get_job_estimate_response
