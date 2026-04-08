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

if TYPE_CHECKING:
  from ..models.failure import Failure
  from ..models.job_metadata import JobMetadata
  from ..models.json_object import JsonObject
  from ..models.noise import Noise





T = TypeVar("T", bound="PickBaseJobExcludeKeyofBaseJobChildJobIds")



@_attrs_define
class PickBaseJobExcludeKeyofBaseJobChildJobIds:
    """ From T, pick a set of properties whose keys are in the union K

        Attributes:
            id (str):
            status (JobStatus):
            type_ (str):
            backend (str):
            dry_run (bool):
            submitter_id (str): The id of the user who submitted the job
            project_id (str):
            parent_job_id (str):
            session_id (str):
            metadata (JobMetadata):
            name (str):
            submitted_at (str):
            started_at (str):
            completed_at (str):
            predicted_wait_time_ms (int):
            predicted_execution_duration_ms (int):
            execution_duration_ms (int):
            failure (Failure):
            output (JsonObject):
            settings (JsonObject):
            stats (JsonObject):
            results (JsonObject):
            shots (int | Unset):
            noise (Noise | Unset):
     """

    id: str
    status: JobStatus
    type_: str
    backend: str
    dry_run: bool
    submitter_id: str
    project_id: str
    parent_job_id: str
    session_id: str
    metadata: JobMetadata
    name: str
    submitted_at: str
    started_at: str
    completed_at: str
    predicted_wait_time_ms: int
    predicted_execution_duration_ms: int
    execution_duration_ms: int
    failure: Failure
    output: JsonObject
    settings: JsonObject
    stats: JsonObject
    results: JsonObject
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.failure import Failure
        from ..models.job_metadata import JobMetadata
        from ..models.json_object import JsonObject
        from ..models.noise import Noise
        id = self.id

        status: str = self.status

        type_ = self.type_

        backend = self.backend

        dry_run = self.dry_run

        submitter_id = self.submitter_id

        project_id = self.project_id

        parent_job_id = self.parent_job_id

        session_id = self.session_id

        metadata = self.metadata.to_dict()

        name = self.name

        submitted_at = self.submitted_at

        started_at = self.started_at

        completed_at = self.completed_at

        predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms = self.execution_duration_ms

        failure = self.failure.to_dict()

        output = self.output.to_dict()

        settings = self.settings.to_dict()

        stats = self.stats.to_dict()

        results = self.results.to_dict()

        shots = self.shots

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "status": status,
            "type": type_,
            "backend": backend,
            "dry_run": dry_run,
            "submitter_id": submitter_id,
            "project_id": project_id,
            "parent_job_id": parent_job_id,
            "session_id": session_id,
            "metadata": metadata,
            "name": name,
            "submitted_at": submitted_at,
            "started_at": started_at,
            "completed_at": completed_at,
            "predicted_wait_time_ms": predicted_wait_time_ms,
            "predicted_execution_duration_ms": predicted_execution_duration_ms,
            "execution_duration_ms": execution_duration_ms,
            "failure": failure,
            "output": output,
            "settings": settings,
            "stats": stats,
            "results": results,
        })
        if shots is not UNSET:
            field_dict["shots"] = shots
        if noise is not UNSET:
            field_dict["noise"] = noise

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.failure import Failure
        from ..models.job_metadata import JobMetadata
        from ..models.json_object import JsonObject
        from ..models.noise import Noise
        d = dict(src_dict)
        id = d.pop("id")

        status = check_job_status(d.pop("status"))




        type_ = d.pop("type")

        backend = d.pop("backend")

        dry_run = d.pop("dry_run")

        submitter_id = d.pop("submitter_id")

        project_id = d.pop("project_id")

        parent_job_id = d.pop("parent_job_id")

        session_id = d.pop("session_id")

        metadata = JobMetadata.from_dict(d.pop("metadata"))




        name = d.pop("name")

        submitted_at = d.pop("submitted_at")

        started_at = d.pop("started_at")

        completed_at = d.pop("completed_at")

        predicted_wait_time_ms = d.pop("predicted_wait_time_ms")

        predicted_execution_duration_ms = d.pop("predicted_execution_duration_ms")

        execution_duration_ms = d.pop("execution_duration_ms")

        failure = Failure.from_dict(d.pop("failure"))




        output = JsonObject.from_dict(d.pop("output"))




        settings = JsonObject.from_dict(d.pop("settings"))




        stats = JsonObject.from_dict(d.pop("stats"))




        results = JsonObject.from_dict(d.pop("results"))




        shots = d.pop("shots", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        pick_base_job_exclude_keyof_base_job_child_job_ids = cls(
            id=id,
            status=status,
            type_=type_,
            backend=backend,
            dry_run=dry_run,
            submitter_id=submitter_id,
            project_id=project_id,
            parent_job_id=parent_job_id,
            session_id=session_id,
            metadata=metadata,
            name=name,
            submitted_at=submitted_at,
            started_at=started_at,
            completed_at=completed_at,
            predicted_wait_time_ms=predicted_wait_time_ms,
            predicted_execution_duration_ms=predicted_execution_duration_ms,
            execution_duration_ms=execution_duration_ms,
            failure=failure,
            output=output,
            settings=settings,
            stats=stats,
            results=results,
            shots=shots,
            noise=noise,
        )


        pick_base_job_exclude_keyof_base_job_child_job_ids.additional_properties = d
        return pick_base_job_exclude_keyof_base_job_child_job_ids

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
