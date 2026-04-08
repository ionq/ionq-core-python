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





T = TypeVar("T", bound="Job")



@_attrs_define
class Job:
    """ 
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
            name (str):
            submitted_at (str):
            started_at (str):
            completed_at (str):
            predicted_wait_time_ms (int):
            predicted_execution_duration_ms (int):
            execution_duration_ms (int):
            output (JsonObject):
            settings (JsonObject):
            stats (JsonObject):
            results (JsonObject):
            metadata (JobMetadata | None | Unset):
            shots (int | Unset):
            noise (Noise | Unset):
            failure (Failure | None | Unset):
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
    name: str
    submitted_at: str
    started_at: str
    completed_at: str
    predicted_wait_time_ms: int
    predicted_execution_duration_ms: int
    execution_duration_ms: int
    output: JsonObject
    settings: JsonObject
    stats: JsonObject
    results: JsonObject
    metadata: JobMetadata | None | Unset = UNSET
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET
    failure: Failure | None | Unset = UNSET





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

        name = self.name

        submitted_at = self.submitted_at

        started_at = self.started_at

        completed_at = self.completed_at

        predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms = self.execution_duration_ms

        output = self.output.to_dict()

        settings = self.settings.to_dict()

        stats = self.stats.to_dict()

        results = self.results.to_dict()

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, JobMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        shots = self.shots

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()

        failure: dict[str, Any] | None | Unset
        if isinstance(self.failure, Unset):
            failure = UNSET
        elif isinstance(self.failure, Failure):
            failure = self.failure.to_dict()
        else:
            failure = self.failure


        field_dict: dict[str, Any] = {}

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
            "name": name,
            "submitted_at": submitted_at,
            "started_at": started_at,
            "completed_at": completed_at,
            "predicted_wait_time_ms": predicted_wait_time_ms,
            "predicted_execution_duration_ms": predicted_execution_duration_ms,
            "execution_duration_ms": execution_duration_ms,
            "output": output,
            "settings": settings,
            "stats": stats,
            "results": results,
        })
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if shots is not UNSET:
            field_dict["shots"] = shots
        if noise is not UNSET:
            field_dict["noise"] = noise
        if failure is not UNSET:
            field_dict["failure"] = failure

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

        name = d.pop("name")

        submitted_at = d.pop("submitted_at")

        started_at = d.pop("started_at")

        completed_at = d.pop("completed_at")

        predicted_wait_time_ms = d.pop("predicted_wait_time_ms")

        predicted_execution_duration_ms = d.pop("predicted_execution_duration_ms")

        execution_duration_ms = d.pop("execution_duration_ms")

        output = JsonObject.from_dict(d.pop("output"))




        settings = JsonObject.from_dict(d.pop("settings"))




        stats = JsonObject.from_dict(d.pop("stats"))




        results = JsonObject.from_dict(d.pop("results"))




        def _parse_metadata(data: object) -> JobMetadata | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_job_metadata_type_1 = JobMetadata.from_dict(data)



                return componentsschemas_optional_job_metadata_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobMetadata | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))


        shots = d.pop("shots", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        def _parse_failure(data: object) -> Failure | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_failure_type_1 = Failure.from_dict(data)



                return componentsschemas_optional_failure_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Failure | None | Unset, data)

        failure = _parse_failure(d.pop("failure", UNSET))


        job = cls(
            id=id,
            status=status,
            type_=type_,
            backend=backend,
            dry_run=dry_run,
            submitter_id=submitter_id,
            project_id=project_id,
            parent_job_id=parent_job_id,
            session_id=session_id,
            name=name,
            submitted_at=submitted_at,
            started_at=started_at,
            completed_at=completed_at,
            predicted_wait_time_ms=predicted_wait_time_ms,
            predicted_execution_duration_ms=predicted_execution_duration_ms,
            execution_duration_ms=execution_duration_ms,
            output=output,
            settings=settings,
            stats=stats,
            results=results,
            metadata=metadata,
            shots=shots,
            noise=noise,
            failure=failure,
        )

        return job

