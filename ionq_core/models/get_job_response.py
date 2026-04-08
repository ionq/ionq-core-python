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
            project_id (None | str | Unset):
            parent_job_id (None | str | Unset):
            session_id (None | str | Unset):
            metadata (JobMetadata | None | Unset):
            name (None | str | Unset):
            submitted_at (str | Unset):
            started_at (None | str | Unset):
            completed_at (None | str | Unset):
            predicted_wait_time_ms (float | None | Unset):
            predicted_execution_duration_ms (float | None | Unset):
            execution_duration_ms (float | None | Unset):
            shots (int | Unset):
            noise (Noise | Unset):
            failure (Failure | None | Unset):
            output (JsonObject | Unset):
            child_job_ids (list[str] | None | Unset):
            settings (CircuitJobSettings | Unset):
            stats (CircuitJobStats | Unset):
            results (CircuitJobResult | None | Unset):
     """

    id: str
    status: JobStatus
    type_: str
    backend: str
    dry_run: bool
    submitter_id: str
    project_id: None | str | Unset = UNSET
    parent_job_id: None | str | Unset = UNSET
    session_id: None | str | Unset = UNSET
    metadata: JobMetadata | None | Unset = UNSET
    name: None | str | Unset = UNSET
    submitted_at: str | Unset = UNSET
    started_at: None | str | Unset = UNSET
    completed_at: None | str | Unset = UNSET
    predicted_wait_time_ms: float | None | Unset = UNSET
    predicted_execution_duration_ms: float | None | Unset = UNSET
    execution_duration_ms: float | None | Unset = UNSET
    shots: int | Unset = UNSET
    noise: Noise | Unset = UNSET
    failure: Failure | None | Unset = UNSET
    output: JsonObject | Unset = UNSET
    child_job_ids: list[str] | None | Unset = UNSET
    settings: CircuitJobSettings | Unset = UNSET
    stats: CircuitJobStats | Unset = UNSET
    results: CircuitJobResult | None | Unset = UNSET





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

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        parent_job_id: None | str | Unset
        if isinstance(self.parent_job_id, Unset):
            parent_job_id = UNSET
        else:
            parent_job_id = self.parent_job_id

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, JobMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        submitted_at = self.submitted_at

        started_at: None | str | Unset
        if isinstance(self.started_at, Unset):
            started_at = UNSET
        else:
            started_at = self.started_at

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = self.completed_at

        predicted_wait_time_ms: float | None | Unset
        if isinstance(self.predicted_wait_time_ms, Unset):
            predicted_wait_time_ms = UNSET
        else:
            predicted_wait_time_ms = self.predicted_wait_time_ms

        predicted_execution_duration_ms: float | None | Unset
        if isinstance(self.predicted_execution_duration_ms, Unset):
            predicted_execution_duration_ms = UNSET
        else:
            predicted_execution_duration_ms = self.predicted_execution_duration_ms

        execution_duration_ms: float | None | Unset
        if isinstance(self.execution_duration_ms, Unset):
            execution_duration_ms = UNSET
        else:
            execution_duration_ms = self.execution_duration_ms

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

        output: dict[str, Any] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        child_job_ids: list[str] | None | Unset
        if isinstance(self.child_job_ids, Unset):
            child_job_ids = UNSET
        elif isinstance(self.child_job_ids, list):
            child_job_ids = self.child_job_ids


        else:
            child_job_ids = self.child_job_ids

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        results: dict[str, Any] | None | Unset
        if isinstance(self.results, Unset):
            results = UNSET
        elif isinstance(self.results, CircuitJobResult):
            results = self.results.to_dict()
        else:
            results = self.results


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
        if child_job_ids is not UNSET:
            field_dict["child_job_ids"] = child_job_ids
        if settings is not UNSET:
            field_dict["settings"] = settings
        if stats is not UNSET:
            field_dict["stats"] = stats
        if results is not UNSET:
            field_dict["results"] = results

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

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))


        def _parse_parent_job_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_job_id = _parse_parent_job_id(d.pop("parent_job_id", UNSET))


        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))


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


        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))


        submitted_at = d.pop("submitted_at", UNSET)

        def _parse_started_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        started_at = _parse_started_at(d.pop("started_at", UNSET))


        def _parse_completed_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))


        def _parse_predicted_wait_time_ms(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        predicted_wait_time_ms = _parse_predicted_wait_time_ms(d.pop("predicted_wait_time_ms", UNSET))


        def _parse_predicted_execution_duration_ms(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        predicted_execution_duration_ms = _parse_predicted_execution_duration_ms(d.pop("predicted_execution_duration_ms", UNSET))


        def _parse_execution_duration_ms(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        execution_duration_ms = _parse_execution_duration_ms(d.pop("execution_duration_ms", UNSET))


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


        _output = d.pop("output", UNSET)
        output: JsonObject | Unset
        if isinstance(_output,  Unset):
            output = UNSET
        else:
            output = JsonObject.from_dict(_output)




        def _parse_child_job_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_optional_string_array_type_0 = cast(list[str], data)

                return componentsschemas_optional_string_array_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        child_job_ids = _parse_child_job_ids(d.pop("child_job_ids", UNSET))


        _settings = d.pop("settings", UNSET)
        settings: CircuitJobSettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = CircuitJobSettings.from_dict(_settings)




        _stats = d.pop("stats", UNSET)
        stats: CircuitJobStats | Unset
        if isinstance(_stats,  Unset):
            stats = UNSET
        else:
            stats = CircuitJobStats.from_dict(_stats)




        def _parse_results(data: object) -> CircuitJobResult | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_optional_circuit_job_result_type_1 = CircuitJobResult.from_dict(data)



                return componentsschemas_optional_circuit_job_result_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CircuitJobResult | None | Unset, data)

        results = _parse_results(d.pop("results", UNSET))


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
            shots=shots,
            noise=noise,
            failure=failure,
            output=output,
            child_job_ids=child_job_ids,
            settings=settings,
            stats=stats,
            results=results,
        )

        return get_job_response

