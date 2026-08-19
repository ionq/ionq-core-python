# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rate_card_entry_unit import check_rate_card_entry_unit
from ..models.rate_card_entry_unit import RateCardEntryUnit
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RateCardEntry")



@_attrs_define
class RateCardEntry:
    """ 
        Attributes:
            sku (str):
            unit (RateCardEntryUnit):
            unit_cost (float | Unset): Present only when unit is "compute_second".
            cost_1q_gate (float | Unset): Present only when unit is "gates".
            cost_2q_gate (float | Unset): Present only when unit is "gates".
            job_cost_minimum (float | Unset): Present only when unit is "gates" and the contract applies a job minimum.
     """

    sku: str
    unit: RateCardEntryUnit
    unit_cost: float | Unset = UNSET
    cost_1q_gate: float | Unset = UNSET
    cost_2q_gate: float | Unset = UNSET
    job_cost_minimum: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        sku = self.sku

        unit: str = self.unit

        unit_cost = self.unit_cost

        cost_1q_gate = self.cost_1q_gate

        cost_2q_gate = self.cost_2q_gate

        job_cost_minimum = self.job_cost_minimum


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sku": sku,
            "unit": unit,
        })
        if unit_cost is not UNSET:
            field_dict["unit_cost"] = unit_cost
        if cost_1q_gate is not UNSET:
            field_dict["cost_1q_gate"] = cost_1q_gate
        if cost_2q_gate is not UNSET:
            field_dict["cost_2q_gate"] = cost_2q_gate
        if job_cost_minimum is not UNSET:
            field_dict["job_cost_minimum"] = job_cost_minimum

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        sku = d.pop("sku")

        unit = check_rate_card_entry_unit(d.pop("unit"))




        unit_cost = d.pop("unit_cost", UNSET)

        cost_1q_gate = d.pop("cost_1q_gate", UNSET)

        cost_2q_gate = d.pop("cost_2q_gate", UNSET)

        job_cost_minimum = d.pop("job_cost_minimum", UNSET)

        rate_card_entry = cls(
            sku=sku,
            unit=unit,
            unit_cost=unit_cost,
            cost_1q_gate=cost_1q_gate,
            cost_2q_gate=cost_2q_gate,
            job_cost_minimum=job_cost_minimum,
        )

        return rate_card_entry

