# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.rate_card_entry import RateCardEntry





T = TypeVar("T", bound="GetJobEstimateResponseRateCard")



@_attrs_define
class GetJobEstimateResponseRateCard:
    """ 
        Attributes:
            rates (list[RateCardEntry]):
            id (str):
     """

    rates: list[RateCardEntry]
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.rate_card_entry import RateCardEntry
        rates = []
        for rates_item_data in self.rates:
            rates_item = rates_item_data.to_dict()
            rates.append(rates_item)



        id = self.id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rates": rates,
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rate_card_entry import RateCardEntry
        d = dict(src_dict)
        rates = []
        _rates = d.pop("rates")
        for rates_item_data in (_rates):
            rates_item = RateCardEntry.from_dict(rates_item_data)



            rates.append(rates_item)


        id = d.pop("id")

        get_job_estimate_response_rate_card = cls(
            rates=rates,
            id=id,
        )


        get_job_estimate_response_rate_card.additional_properties = d
        return get_job_estimate_response_rate_card

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
