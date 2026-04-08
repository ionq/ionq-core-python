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
            project_id (str | Unset):
            parent_job_id (str | Unset):
            session_id (str | Unset):
            metadata (JobMetadata | Unset):
            name (str | Unset):
            submitted_at (str | Unset):
            started_at (str | Unset):
            completed_at (str | Unset):
            predicted_wait_time_ms (int | Unset):
            predicted_execution_duration_ms (int | Unset):
            execution_duration_ms (int | Unset):
            shots (int | Unset):
            noise (Noise | Unset):
            failure (Failure | Unset):
            output (JsonObject | Unset):
            settings (JsonObject | Unset):
            stats (JsonObject | Unset):
            results (JsonObject | Unset):
     """

    id: str
    status: JobStatus
    type_: str
    backend: str
    dry_run: bool
    submitter_id: str
    project_id: str | Unset = UNSET
    parent_job_id: str | Unset = UNSET
    session_id: str | Unset = UNSET
    metadata: JobMetadata | Unset = UNSET
    name: str | Unset = UNSET
    submitted_at: str | Unset = UNSET
    started_at: str | Unset = UNSET
    completed_at: str | Unset = UNSET
    predicted_wait_time_ms: int | Unset = UNSET
    predicted_execution_duration_ms: int | Unset = UNSET
    execution_duration_ms: int | Unset = UNSET
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET
    failure: Failure | Unset = UNSET
    output: JsonObject | Unset = UNSET
    settings: JsonObject | Unset = UNSET
    stats: JsonObject | Unset = UNSET
    results: JsonObject | Unset = UNSET





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

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name

        submitted_at = self.submitted_at

        started_at = self.started_at

        completed_at = self.completed_at

        predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms = self.execution_duration_ms

        shots = self.shots

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()

        failure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.failure, Unset):
            failure = self.failure.to_dict()

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        results: dict[str, Any] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = self.results.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "status": status,
            "type": type_,
            "backend": backend,
            "dry_run": dry_run,
            "submitter_id": submitter_id,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if parent_job_id is not UNSET:
            field_dict["parent_job_id"] = parent_job_id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if submitted_at is not UNSET:
            field_dict["submitted_at"] = submitted_at
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if predicted_wait_time_ms is not UNSET:
            field_dict["predicted_wait_time_ms"] = predicted_wait_time_ms
        if predicted_execution_duration_ms is not UNSET:
            field_dict["predicted_execution_duration_ms"] = predicted_execution_duration_ms
        if execution_duration_ms is not UNSET:
            field_dict["execution_duration_ms"] = execution_duration_ms
        if shots is not UNSET:
            field_dict["shots"] = shots
        if noise is not UNSET:
            field_dict["noise"] = noise
        if failure is not UNSET:
            field_dict["failure"] = failure
        if output is not UNSET:
            field_dict["output"] = output
        if settings is not UNSET:
            field_dict["settings"] = settings
        if stats is not UNSET:
            field_dict["stats"] = stats
        if results is not UNSET:
            field_dict["results"] = results

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

        project_id = d.pop("project_id", UNSET)

        parent_job_id = d.pop("parent_job_id", UNSET)

        session_id = d.pop("session_id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: JobMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = JobMetadata.from_dict(_metadata)




        name = d.pop("name", UNSET)

        submitted_at = d.pop("submitted_at", UNSET)

        started_at = d.pop("started_at", UNSET)

        completed_at = d.pop("completed_at", UNSET)

        predicted_wait_time_ms = d.pop("predicted_wait_time_ms", UNSET)

        predicted_execution_duration_ms = d.pop("predicted_execution_duration_ms", UNSET)

        execution_duration_ms = d.pop("execution_duration_ms", UNSET)

        shots = d.pop("shots", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        _failure = d.pop("failure", UNSET)
        failure: Failure | Unset
        if isinstance(_failure,  Unset):
            failure = UNSET
        else:
            failure = Failure.from_dict(_failure)




        _output = d.pop("output", UNSET)
        output: JsonObject | Unset
        if isinstance(_output,  Unset):
            output = UNSET
        else:
            output = JsonObject.from_dict(_output)




        _settings = d.pop("settings", UNSET)
        settings: JsonObject | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = JsonObject.from_dict(_settings)




        _stats = d.pop("stats", UNSET)
        stats: JsonObject | Unset
        if isinstance(_stats,  Unset):
            stats = UNSET
        else:
            stats = JsonObject.from_dict(_stats)




        _results = d.pop("results", UNSET)
        results: JsonObject | Unset
        if isinstance(_results,  Unset):
            results = UNSET
        else:
            results = JsonObject.from_dict(_results)




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
            metadata=metadata,
            name=name,
            submitted_at=submitted_at,
            started_at=started_at,
            completed_at=completed_at,
            predicted_wait_time_ms=predicted_wait_time_ms,
            predicted_execution_duration_ms=predicted_execution_duration_ms,
            execution_duration_ms=execution_duration_ms,
            shots=shots,
            noise=noise,
            failure=failure,
            output=output,
            settings=settings,
            stats=stats,
            results=results,
        )

        return job

