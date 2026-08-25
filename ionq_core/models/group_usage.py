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
  from ..models.usage_amount import UsageAmount





T = TypeVar("T", bound="GroupUsage")



@_attrs_define
class GroupUsage:
    """ A group's single date usage

        Attributes:
            amount (float | Unset): The cost amount for the group of the given date, in units given by amount_unit Example:
                144.39.
            amount_unit (str | Unset): The unit amount is denominated in. Normalized to credits if any credit activity is
                present anywhere in the request Example: USD.
            amounts (list[UsageAmount] | Unset): The per-currency breakdown of amount before ACU normalization
            group_id (str | Unset): The unique ID from the group Example: 2bfd0fd5-5854-4916-917f-a907af586755.
            group_name (str | Unset): The group's descriptive name Example: Project Jumping Lemming.
            job_count (int | Unset): The number of jobs run for the group on the given date Example: 9.
            time_us (float | Unset): The QPU time in microseconds Example: 1566154.312523.
     """

    amount: float | Unset = UNSET
    amount_unit: str | Unset = UNSET
    amounts: list[UsageAmount] | Unset = UNSET
    group_id: str | Unset = UNSET
    group_name: str | Unset = UNSET
    job_count: int | Unset = UNSET
    time_us: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_amount import UsageAmount
        amount = self.amount

        amount_unit = self.amount_unit

        amounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.amounts, Unset):
            amounts = []
            for amounts_item_data in self.amounts:
                amounts_item = amounts_item_data.to_dict()
                amounts.append(amounts_item)



        group_id = self.group_id

        group_name = self.group_name

        job_count = self.job_count

        time_us = self.time_us


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if amount is not UNSET:
            field_dict["amount"] = amount
        if amount_unit is not UNSET:
            field_dict["amount_unit"] = amount_unit
        if amounts is not UNSET:
            field_dict["amounts"] = amounts
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if job_count is not UNSET:
            field_dict["job_count"] = job_count
        if time_us is not UNSET:
            field_dict["time_us"] = time_us

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_amount import UsageAmount
        d = dict(src_dict)
        amount = d.pop("amount", UNSET)

        amount_unit = d.pop("amount_unit", UNSET)

        _amounts = d.pop("amounts", UNSET)
        amounts: list[UsageAmount] | Unset = UNSET
        if _amounts is not UNSET:
            amounts = []
            for amounts_item_data in _amounts:
                amounts_item = UsageAmount.from_dict(amounts_item_data)



                amounts.append(amounts_item)


        group_id = d.pop("group_id", UNSET)

        group_name = d.pop("group_name", UNSET)

        job_count = d.pop("job_count", UNSET)

        time_us = d.pop("time_us", UNSET)

        group_usage = cls(
            amount=amount,
            amount_unit=amount_unit,
            amounts=amounts,
            group_id=group_id,
            group_name=group_name,
            job_count=job_count,
            time_us=time_us,
        )


        group_usage.additional_properties = d
        return group_usage

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
