# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_q_ctrl_status import check_job_q_ctrl_status
from ..models.job_q_ctrl_status import JobQCtrlStatus
from typing import cast






T = TypeVar("T", bound="AddJobResultsPayload")



@_attrs_define
class AddJobResultsPayload:
    """ 
        Attributes:
            processing_status (JobQCtrlStatus):
            optimal_cost (float):
            optimal_bitstring (str):
     """

    processing_status: JobQCtrlStatus
    optimal_cost: float
    optimal_bitstring: str





    def to_dict(self) -> dict[str, Any]:
        processing_status: str = self.processing_status

        optimal_cost = self.optimal_cost

        optimal_bitstring = self.optimal_bitstring


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "processing_status": processing_status,
            "optimal_cost": optimal_cost,
            "optimal_bitstring": optimal_bitstring,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        processing_status = check_job_q_ctrl_status(d.pop("processing_status"))




        optimal_cost = d.pop("optimal_cost")

        optimal_bitstring = d.pop("optimal_bitstring")

        add_job_results_payload = cls(
            processing_status=processing_status,
            optimal_cost=optimal_cost,
            optimal_bitstring=optimal_bitstring,
        )

        return add_job_results_payload

