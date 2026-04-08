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
  from ..models.circuit_job_result import CircuitJobResult
  from ..models.circuit_job_settings import CircuitJobSettings
  from ..models.circuit_job_stats import CircuitJobStats
  from ..models.failure import Failure
  from ..models.job_metadata import JobMetadata
  from ..models.json_object import JsonObject
  from ..models.noise import Noise





T = TypeVar("T", bound="GetJobResponse")



@_attrs_define
class GetJobResponse:
    """ 
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
            metadata (JobMetadata | None):
            name (None | str):
            submitted_at (str):
            started_at (None | str):
            completed_at (None | str):
            predicted_wait_time_ms (float | None):
            predicted_execution_duration_ms (float | None):
            execution_duration_ms (float | None):
            failure (Failure | None):
            output (JsonObject):
            child_job_ids (list[str] | None):
            settings (CircuitJobSettings):
            stats (CircuitJobStats):
            results (CircuitJobResult | None):
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
    metadata: JobMetadata | None
    name: None | str
    submitted_at: str
    started_at: None | str
    completed_at: None | str
    predicted_wait_time_ms: float | None
    predicted_execution_duration_ms: float | None
    execution_duration_ms: float | None
    failure: Failure | None
    output: JsonObject
    child_job_ids: list[str] | None
    settings: CircuitJobSettings
    stats: CircuitJobStats
    results: CircuitJobResult | None
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.circuit_job_result import CircuitJobResult
        from ..models.circuit_job_settings import CircuitJobSettings
        from ..models.circuit_job_stats import CircuitJobStats
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

        project_id: None | str
        project_id = self.project_id

        parent_job_id: None | str
        parent_job_id = self.parent_job_id

        session_id: None | str
        session_id = self.session_id

        metadata: dict[str, Any] | None
        if isinstance(self.metadata, JobMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        name: None | str
        name = self.name

        submitted_at = self.submitted_at

        started_at: None | str
        started_at = self.started_at

        completed_at: None | str
        completed_at = self.completed_at

        predicted_wait_time_ms: float | None
        predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms: float | None
        predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms: float | None
        execution_duration_ms = self.execution_duration_ms

        failure: dict[str, Any] | None
        if isinstance(self.failure, Failure):
            failure = self.failure.to_dict()
        else:
            failure = self.failure

        output = self.output.to_dict()

        child_job_ids: list[str] | None
        if isinstance(self.child_job_ids, list):
            child_job_ids = self.child_job_ids


        else:
            child_job_ids = self.child_job_ids

        settings = self.settings.to_dict()

        stats = self.stats.to_dict()

        results: dict[str, Any] | None
        if isinstance(self.results, CircuitJobResult):
            results = self.results.to_dict()
        else:
            results = self.results

        shots = self.shots

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()


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
            "child_job_ids": child_job_ids,
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
        from ..models.circuit_job_result import CircuitJobResult
        from ..models.circuit_job_settings import CircuitJobSettings
        from ..models.circuit_job_stats import CircuitJobStats
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


        def _parse_metadata(data: object) -> JobMetadata | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_job_metadata_type_1 = JobMetadata.from_dict(data)



                return componentsschemas_optional_job_metadata_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JobMetadata | None, data)

        metadata = _parse_metadata(d.pop("metadata"))


        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))


        submitted_at = d.pop("submitted_at")

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


        def _parse_predicted_wait_time_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        predicted_wait_time_ms = _parse_predicted_wait_time_ms(d.pop("predicted_wait_time_ms"))


        def _parse_predicted_execution_duration_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        predicted_execution_duration_ms = _parse_predicted_execution_duration_ms(d.pop("predicted_execution_duration_ms"))


        def _parse_execution_duration_ms(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        execution_duration_ms = _parse_execution_duration_ms(d.pop("execution_duration_ms"))


        def _parse_failure(data: object) -> Failure | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_failure_type_1 = Failure.from_dict(data)



                return componentsschemas_optional_failure_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Failure | None, data)

        failure = _parse_failure(d.pop("failure"))


        output = JsonObject.from_dict(d.pop("output"))




        def _parse_child_job_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_optional_string_array_type_0 = cast(list[str], data)

                return componentsschemas_optional_string_array_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        child_job_ids = _parse_child_job_ids(d.pop("child_job_ids"))


        settings = CircuitJobSettings.from_dict(d.pop("settings"))




        stats = CircuitJobStats.from_dict(d.pop("stats"))




        def _parse_results(data: object) -> CircuitJobResult | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_circuit_job_result_type_1 = CircuitJobResult.from_dict(data)



                return componentsschemas_optional_circuit_job_result_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CircuitJobResult | None, data)

        results = _parse_results(d.pop("results"))


        shots = d.pop("shots", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        get_job_response = cls(
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
            child_job_ids=child_job_ids,
            settings=settings,
            stats=stats,
            results=results,
            shots=shots,
            noise=noise,
        )

        return get_job_response

