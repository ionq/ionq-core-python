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
import datetime

if TYPE_CHECKING:
  from ..models.group_usage import GroupUsage
  from ..models.usage_amount import UsageAmount





T = TypeVar("T", bound="Usage")



@_attrs_define
class Usage:
    """ Single date of QPU usage

        Attributes:
            amount (float): The amount as a cost, in units given by amount_unit Example: 1614.23.
            from_ (datetime.date): Date for this group's usage Example: 2023-07-01.
            group_usages (list[GroupUsage]): The top 5 usage groups in order of cost amount descending
            job_count (int): The count of jobs for this group on the given from date Example: 10.
            time_us (float): The QPU time in microseconds Example: 5143166.13413.
            amount_unit (str | Unset): The unit amount is denominated in. Normalized to credits if any credit activity is
                present anywhere in the request Example: USD.
            amounts (list[UsageAmount] | Unset): The per-currency breakdown of amount before ACU normalization
     """

    amount: float
    from_: datetime.date
    group_usages: list[GroupUsage]
    job_count: int
    time_us: float
    amount_unit: str | Unset = UNSET
    amounts: list[UsageAmount] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.group_usage import GroupUsage
        from ..models.usage_amount import UsageAmount
        amount = self.amount

        from_ = self.from_.isoformat()

        group_usages = []
        for group_usages_item_data in self.group_usages:
            group_usages_item = group_usages_item_data.to_dict()
            group_usages.append(group_usages_item)



        job_count = self.job_count

        time_us = self.time_us

        amount_unit = self.amount_unit

        amounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.amounts, Unset):
            amounts = []
            for amounts_item_data in self.amounts:
                amounts_item = amounts_item_data.to_dict()
                amounts.append(amounts_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "amount": amount,
            "from": from_,
            "group_usages": group_usages,
            "job_count": job_count,
            "time_us": time_us,
        })
        if amount_unit is not UNSET:
            field_dict["amount_unit"] = amount_unit
        if amounts is not UNSET:
            field_dict["amounts"] = amounts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_usage import GroupUsage
        from ..models.usage_amount import UsageAmount
        d = dict(src_dict)
        amount = d.pop("amount")

        from_ = datetime.date.fromisoformat(d.pop("from"))




        group_usages = []
        _group_usages = d.pop("group_usages")
        for group_usages_item_data in (_group_usages):
            group_usages_item = GroupUsage.from_dict(group_usages_item_data)



            group_usages.append(group_usages_item)


        job_count = d.pop("job_count")

        time_us = d.pop("time_us")

        amount_unit = d.pop("amount_unit", UNSET)

        _amounts = d.pop("amounts", UNSET)
        amounts: list[UsageAmount] | Unset = UNSET
        if _amounts is not UNSET:
            amounts = []
            for amounts_item_data in _amounts:
                amounts_item = UsageAmount.from_dict(amounts_item_data)



                amounts.append(amounts_item)


        usage = cls(
            amount=amount,
            from_=from_,
            group_usages=group_usages,
            job_count=job_count,
            time_us=time_us,
            amount_unit=amount_unit,
            amounts=amounts,
        )


        usage.additional_properties = d
        return usage

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
