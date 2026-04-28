# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.group_by import check_group_by
from ..models.group_by import GroupBy
from ..models.modality import check_modality
from ..models.modality import Modality
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.usage import Usage





T = TypeVar("T", bound="Usages")



@_attrs_define
class Usages:
    """ QPU usage details for a given modality and date range.

        Attributes:
            group_type (GroupBy): QPU Usage grouping Example: project.
            modality (Modality): Report modality Example: daily.
            amount_total (float | Unset): The total cost amount for the given timeframe, in units given by usage_unit
                Example: 151.31.
            job_count (int | Unset): The total number of jobs run in the timeframe Example: 514.
            organization (UUID | Unset): UUID of an organization. Example: 71d164e-6ebe-4126-8839-f1529bb01a00.
            time_us_total (float | Unset): The total QPU time usage for the given timeframe, in microseconds Example:
                1566154.312523.
            usage_data (list[Usage] | Unset): The breakdown of usage by group type in date order most to least recent
            usage_from (datetime.datetime | Unset): Usage beginning RFC 3339 timestamp Example: 2025-10-01T00:00:00Z.
            usage_to (datetime.datetime | Unset): Usage end RFC 3339 timestamp Example: 2025-11-01T00:00:00Z.
            usage_unit (str | Unset): The currency of the total and job cost amounts Example: USD.
     """

    group_type: GroupBy
    modality: Modality
    amount_total: float | Unset = UNSET
    job_count: int | Unset = UNSET
    organization: UUID | Unset = UNSET
    time_us_total: float | Unset = UNSET
    usage_data: list[Usage] | Unset = UNSET
    usage_from: datetime.datetime | Unset = UNSET
    usage_to: datetime.datetime | Unset = UNSET
    usage_unit: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.usage import Usage
        group_type: str = self.group_type

        modality: str = self.modality

        amount_total = self.amount_total

        job_count = self.job_count

        organization: str | Unset = UNSET
        if not isinstance(self.organization, Unset):
            organization = str(self.organization)

        time_us_total = self.time_us_total

        usage_data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.usage_data, Unset):
            usage_data = []
            for usage_data_item_data in self.usage_data:
                usage_data_item = usage_data_item_data.to_dict()
                usage_data.append(usage_data_item)



        usage_from: str | Unset = UNSET
        if not isinstance(self.usage_from, Unset):
            usage_from = self.usage_from.isoformat()

        usage_to: str | Unset = UNSET
        if not isinstance(self.usage_to, Unset):
            usage_to = self.usage_to.isoformat()

        usage_unit = self.usage_unit


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "group_type": group_type,
            "modality": modality,
        })
        if amount_total is not UNSET:
            field_dict["amount_total"] = amount_total
        if job_count is not UNSET:
            field_dict["job_count"] = job_count
        if organization is not UNSET:
            field_dict["organization"] = organization
        if time_us_total is not UNSET:
            field_dict["time_us_total"] = time_us_total
        if usage_data is not UNSET:
            field_dict["usage_data"] = usage_data
        if usage_from is not UNSET:
            field_dict["usage_from"] = usage_from
        if usage_to is not UNSET:
            field_dict["usage_to"] = usage_to
        if usage_unit is not UNSET:
            field_dict["usage_unit"] = usage_unit

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage import Usage
        d = dict(src_dict)
        group_type = check_group_by(d.pop("group_type"))




        modality = check_modality(d.pop("modality"))




        amount_total = d.pop("amount_total", UNSET)

        job_count = d.pop("job_count", UNSET)

        _organization = d.pop("organization", UNSET)
        organization: UUID | Unset
        if isinstance(_organization,  Unset):
            organization = UNSET
        else:
            organization = UUID(_organization)




        time_us_total = d.pop("time_us_total", UNSET)

        _usage_data = d.pop("usage_data", UNSET)
        usage_data: list[Usage] | Unset = UNSET
        if _usage_data is not UNSET:
            usage_data = []
            for usage_data_item_data in _usage_data:
                usage_data_item = Usage.from_dict(usage_data_item_data)



                usage_data.append(usage_data_item)


        _usage_from = d.pop("usage_from", UNSET)
        usage_from: datetime.datetime | Unset
        if isinstance(_usage_from,  Unset):
            usage_from = UNSET
        else:
            usage_from = isoparse(_usage_from)




        _usage_to = d.pop("usage_to", UNSET)
        usage_to: datetime.datetime | Unset
        if isinstance(_usage_to,  Unset):
            usage_to = UNSET
        else:
            usage_to = isoparse(_usage_to)




        usage_unit = d.pop("usage_unit", UNSET)

        usages = cls(
            group_type=group_type,
            modality=modality,
            amount_total=amount_total,
            job_count=job_count,
            organization=organization,
            time_us_total=time_us_total,
            usage_data=usage_data,
            usage_from=usage_from,
            usage_to=usage_to,
            usage_unit=usage_unit,
        )


        usages.additional_properties = d
        return usages

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
