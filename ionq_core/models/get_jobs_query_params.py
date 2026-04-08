from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_status import check_job_status
from ..models.job_status import JobStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GetJobsQueryParams")



@_attrs_define
class GetJobsQueryParams:
    """ 
        Attributes:
            ids (list[str] | Unset):
            parent_job_id (str | Unset):
            status (JobStatus | Unset):
            target (str | Unset): Filter jobs by backend target. Supports single target or comma-separated list of targets.
                Example: simulator.
            session_id (str | Unset):
            submitter_id (str | Unset): The id of another user within a shared project to view their submitted jobs. Ignored
                if not a project member.
            limit (int | Unset):
            next_ (str | Unset):
     """

    ids: list[str] | Unset = UNSET
    parent_job_id: str | Unset = UNSET
    status: JobStatus | Unset = UNSET
    target: str | Unset = UNSET
    session_id: str | Unset = UNSET
    submitter_id: str | Unset = UNSET
    limit: int | Unset = UNSET
    next_: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        ids: list[str] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids



        parent_job_id = self.parent_job_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status


        target = self.target

        session_id = self.session_id

        submitter_id = self.submitter_id

        limit = self.limit

        next_ = self.next_


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if ids is not UNSET:
            field_dict["ids"] = ids
        if parent_job_id is not UNSET:
            field_dict["parent_job_id"] = parent_job_id
        if status is not UNSET:
            field_dict["status"] = status
        if target is not UNSET:
            field_dict["target"] = target
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if submitter_id is not UNSET:
            field_dict["submitter_id"] = submitter_id
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ids = cast(list[str], d.pop("ids", UNSET))


        parent_job_id = d.pop("parent_job_id", UNSET)

        _status = d.pop("status", UNSET)
        status: JobStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_job_status(_status)




        target = d.pop("target", UNSET)

        session_id = d.pop("session_id", UNSET)

        submitter_id = d.pop("submitter_id", UNSET)

        limit = d.pop("limit", UNSET)

        next_ = d.pop("next", UNSET)

        get_jobs_query_params = cls(
            ids=ids,
            parent_job_id=parent_job_id,
            status=status,
            target=target,
            session_id=session_id,
            submitter_id=submitter_id,
            limit=limit,
            next_=next_,
        )

        return get_jobs_query_params

