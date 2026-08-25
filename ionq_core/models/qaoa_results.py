# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qaoa_results_processing_status import check_qaoa_results_processing_status
from ..models.qaoa_results_processing_status import QaoaResultsProcessingStatus
from typing import cast






T = TypeVar("T", bound="QaoaResults")



@_attrs_define
class QaoaResults:
    """ Optimization output recorded by a Q-CTRL QAOA job after it completes.

        Attributes:
            optimal_cost (float): Best objective value the optimizer reached.
            optimal_bitstring (str): Bitstring corresponding to the best solution found.
            processing_status (QaoaResultsProcessingStatus): Current state of the optimization loop.
     """

    optimal_cost: float
    optimal_bitstring: str
    processing_status: QaoaResultsProcessingStatus





    def to_dict(self) -> dict[str, Any]:
        optimal_cost = self.optimal_cost

        optimal_bitstring = self.optimal_bitstring

        processing_status: str = self.processing_status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "optimal_cost": optimal_cost,
            "optimal_bitstring": optimal_bitstring,
            "processing_status": processing_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        optimal_cost = d.pop("optimal_cost")

        optimal_bitstring = d.pop("optimal_bitstring")

        processing_status = check_qaoa_results_processing_status(d.pop("processing_status"))




        qaoa_results = cls(
            optimal_cost=optimal_cost,
            optimal_bitstring=optimal_bitstring,
            processing_status=processing_status,
        )

        return qaoa_results
