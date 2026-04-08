from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.json_multi_circuit_job_type import check_json_multi_circuit_job_type
from ..models.json_multi_circuit_job_type import JSONMultiCircuitJobType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.job_metadata import JobMetadata
  from ..models.json_multi_circuit_input import JsonMultiCircuitInput
  from ..models.json_multi_circuit_job_settings import JSONMultiCircuitJobSettings
  from ..models.noise import Noise





T = TypeVar("T", bound="JSONMultiCircuitJob")



@_attrs_define
class JSONMultiCircuitJob:
    """ Submit multiple circuits in a single job. Each circuit inherits the parent `input.gateset` unless overridden by
    `circuits[].gateset`.

        Example:
            {'type': 'ionq.multi-circuit.v1', 'backend': 'simulator', 'shots': 500, 'input': {'gateset': 'native', 'qubits':
                2, 'circuits': [{'name': 'qis circuit override', 'gateset': 'qis', 'circuit': [{'gate': 'h', 'target': 0},
                {'gate': 'cnot', 'target': 0, 'control': 1}]}, {'name': 'native circuit from parent', 'circuit': [{'gate': 'ms',
                'targets': [0, 1], 'phases': [0, 0.25]}, {'gate': 'gpi2', 'target': 0, 'phase': 0.75}]}]}}

        Attributes:
            backend (str):
            type_ (JSONMultiCircuitJobType):
            input_ (JsonMultiCircuitInput):
            name (str | Unset):
            metadata (JobMetadata | Unset):
            shots (int | Unset):  Default: 100.
            session_id (str | Unset):
            settings (JSONMultiCircuitJobSettings | Unset):
            dry_run (bool | Unset):
            noise (Noise | Unset):
     """

    backend: str
    type_: JSONMultiCircuitJobType
    input_: JsonMultiCircuitInput
    name: str | Unset = UNSET
    metadata: JobMetadata | Unset = UNSET
    shots: int | Unset = 100
    session_id: str | Unset = UNSET
    settings: JSONMultiCircuitJobSettings | Unset = UNSET
    dry_run: bool | Unset = UNSET
    noise: Noise | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_metadata import JobMetadata
        from ..models.json_multi_circuit_input import JsonMultiCircuitInput
        from ..models.json_multi_circuit_job_settings import JSONMultiCircuitJobSettings
        from ..models.noise import Noise
        backend = self.backend

        type_: str = self.type_

        input_ = self.input_.to_dict()

        name = self.name

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        shots = self.shots

        session_id = self.session_id

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        dry_run = self.dry_run

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "backend": backend,
            "type": type_,
            "input": input_,
        })
        if name is not UNSET:
            field_dict["name"] = name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if shots is not UNSET:
            field_dict["shots"] = shots
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if settings is not UNSET:
            field_dict["settings"] = settings
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if noise is not UNSET:
            field_dict["noise"] = noise

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_metadata import JobMetadata
        from ..models.json_multi_circuit_input import JsonMultiCircuitInput
        from ..models.json_multi_circuit_job_settings import JSONMultiCircuitJobSettings
        from ..models.noise import Noise
        d = dict(src_dict)
        backend = d.pop("backend")

        type_ = check_json_multi_circuit_job_type(d.pop("type"))




        input_ = JsonMultiCircuitInput.from_dict(d.pop("input"))




        name = d.pop("name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: JobMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = JobMetadata.from_dict(_metadata)




        shots = d.pop("shots", UNSET)

        session_id = d.pop("session_id", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: JSONMultiCircuitJobSettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = JSONMultiCircuitJobSettings.from_dict(_settings)




        dry_run = d.pop("dry_run", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        json_multi_circuit_job = cls(
            backend=backend,
            type_=type_,
            input_=input_,
            name=name,
            metadata=metadata,
            shots=shots,
            session_id=session_id,
            settings=settings,
            dry_run=dry_run,
            noise=noise,
        )

        return json_multi_circuit_job

