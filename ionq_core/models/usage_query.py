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
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="UsageQuery")



@_attrs_define
class UsageQuery:
    """ Details of current API Key session.

        Attributes:
            end_date (datetime.date): End date, exclusive Example: 2023-08-01.
            group_by (GroupBy): QPU Usage grouping Example: project.
            modality (Modality): Report modality Example: daily.
            start_date (datetime.date): Start date, inclusive Example: 2023-07-01.
     """

    end_date: datetime.date
    group_by: GroupBy
    modality: Modality
    start_date: datetime.date
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        end_date = self.end_date.isoformat()

        group_by: str = self.group_by

        modality: str = self.modality

        start_date = self.start_date.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "end_date": end_date,
            "group_by": group_by,
            "modality": modality,
            "start_date": start_date,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end_date = isoparse(d.pop("end_date")).date()




        group_by = check_group_by(d.pop("group_by"))




        modality = check_modality(d.pop("modality"))




        start_date = isoparse(d.pop("start_date")).date()




        usage_query = cls(
            end_date=end_date,
            group_by=group_by,
            modality=modality,
            start_date=start_date,
        )


        usage_query.additional_properties = d
        return usage_query

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
