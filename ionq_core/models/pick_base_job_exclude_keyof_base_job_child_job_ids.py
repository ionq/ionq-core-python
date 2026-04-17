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
  from ..models.failure_type_0 import FailureType0
  from ..models.job_metadata_type_0 import JobMetadataType0
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
            project_id (None | str):
            parent_job_id (None | str):
            session_id (None | str):
            metadata (JobMetadataType0 | None):
            name (None | str):
            submitted_at (None | str):
            started_at (None | str):
            completed_at (None | str):
            predicted_wait_time_ms (int | None):
            predicted_execution_duration_ms (int | None):
            execution_duration_ms (int | None):
            failure (FailureType0 | None):
            output (JsonObject):
            settings (JsonObject):
            stats (JsonObject):
            results (JsonObject | None):
            shots (int | Unset):
            noise (Noise | Unset):
     """

    id: str
    status: JobStatus
    type_: str
    backend: str
    dry_run: bool
    submitter_id: str
    project_id: None | str
    parent_job_id: None | str
    session_id: None | str
    metadata: JobMetadataType0 | None
    name: None | str
    submitted_at: None | str
    started_at: None | str
    completed_at: None | str
    predicted_wait_time_ms: int | None
    predicted_execution_duration_ms: int | None
    execution_duration_ms: int | None
    failure: FailureType0 | None
    output: JsonObject
    settings: JsonObject
    stats: JsonObject
    results: JsonObject | None
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.failure_type_0 import FailureType0
        from ..models.job_metadata_type_0 import JobMetadataType0
        from ..models.json_object import JsonObject
        from ..models.noise import Noise
        id = self.id

        status: str = self.status

        type_ = self.type_

        backend = self.backend

        dry_run = self.dry_run

        submitter_id = self.submitter_id

        project_id: None | str
        project_id = self.project_id

        parent_job_id: None | str
        parent_job_id = self.parent_job_id

        session_id: None | str
        session_id = self.session_id

        metadata: dict[str, Any] | None
        if isinstance(self.metadata, JobMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        name: None | str
        name = self.name

        submitted_at: None | str
        submitted_at = self.submitted_at

        started_at: None | str
        started_at = self.started_at

        completed_at: None | str
        completed_at = self.completed_at

        predicted_wait_time_ms: int | None
        predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms: int | None
        predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms: int | None
        execution_duration_ms = self.execution_duration_ms

        failure: dict[str, Any] | None
        if isinstance(self.failure, FailureType0):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        output = self.output.to_dict()

        settings = self.settings.to_dict()

        stats = self.stats.to_dict()

        results: dict[str, Any] | None
        if isinstance(self.results, JsonObject):
            results = self.results.to_dict()
        else:
            results = self.results

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
        from ..models.failure_type_0 import FailureType0
        from ..models.job_metadata_type_0 import JobMetadataType0
        from ..models.json_object import JsonObject
        from ..models.noise import Noise
        d = dict(src_dict)
        id = d.pop("id")

        status = check_job_status(d.pop("status"))




        type_ = d.pop("type")

        backend = d.pop("backend")

        dry_run = d.pop("dry_run")

        submitter_id = d.pop("submitter_id")

        def _parse_project_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        project_id = _parse_project_id(d.pop("project_id"))


        def _parse_parent_job_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parent_job_id = _parse_parent_job_id(d.pop("parent_job_id"))


        def _parse_session_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        session_id = _parse_session_id(d.pop("session_id"))


        def _parse_metadata(data: object) -> JobMetadataType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_job_metadata_type_0 = JobMetadataType0.from_dict(data)



                return componentsschemas_job_metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobMetadataType0 | None, data)

        metadata = _parse_metadata(d.pop("metadata"))


        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))


        def _parse_submitted_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        submitted_at = _parse_submitted_at(d.pop("submitted_at"))


        def _parse_started_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        started_at = _parse_started_at(d.pop("started_at"))


        def _parse_completed_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))


        def _parse_predicted_wait_time_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        predicted_wait_time_ms = _parse_predicted_wait_time_ms(d.pop("predicted_wait_time_ms"))


        def _parse_predicted_execution_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        predicted_execution_duration_ms = _parse_predicted_execution_duration_ms(d.pop("predicted_execution_duration_ms"))


        def _parse_execution_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        execution_duration_ms = _parse_execution_duration_ms(d.pop("execution_duration_ms"))


        def _parse_failure(data: object) -> FailureType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_failure_type_0 = FailureType0.from_dict(data)



                return componentsschemas_failure_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FailureType0 | None, data)

        failure = _parse_failure(d.pop("failure"))


        output = JsonObject.from_dict(d.pop("output"))




        settings = JsonObject.from_dict(d.pop("settings"))




        stats = JsonObject.from_dict(d.pop("stats"))




        def _parse_results(data: object) -> JsonObject | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                results_type_1 = JsonObject.from_dict(data)



                return results_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonObject | None, data)

        results = _parse_results(d.pop("results"))


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
