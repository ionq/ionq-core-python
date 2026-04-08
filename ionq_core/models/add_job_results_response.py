from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AddJobResultsResponse")



@_attrs_define
class AddJobResultsResponse:
    """ 
        Attributes:
            job_id (str):
     """

    job_id: str





    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "job_id": job_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        add_job_results_response = cls(
            job_id=job_id,
        )

        return add_job_results_response

