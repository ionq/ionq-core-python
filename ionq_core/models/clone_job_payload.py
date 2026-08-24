# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.clone_job_payload_settings import CloneJobPayloadSettings
  from ..models.job_metadata import JobMetadata
  from ..models.noise import Noise





T = TypeVar("T", bound="CloneJobPayload")



@_attrs_define
class CloneJobPayload:
    """ Make all properties in T optional

        Attributes:
            parent (str | Unset):
            name (str | Unset):
            metadata (JobMetadata | Unset):
            shots (int | Unset): `shots` is ignored by ideal simulator backend. Default: 100.
            backend (str | Unset):
            session_id (str | Unset):
            settings (CloneJobPayloadSettings | Unset):
            dry_run (bool | Unset):
            noise (Noise | Unset):
     """

    parent: str | Unset = UNSET
    name: str | Unset = UNSET
    metadata: JobMetadata | Unset = UNSET
    shots: int | Unset = 100
    backend: str | Unset = UNSET
    session_id: str | Unset = UNSET
    settings: CloneJobPayloadSettings | Unset = UNSET
    dry_run: bool | Unset = UNSET
    noise: Noise | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.clone_job_payload_settings import CloneJobPayloadSettings
        from ..models.job_metadata import JobMetadata
        from ..models.noise import Noise
        parent = self.parent

        name = self.name

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        shots = self.shots

        backend = self.backend

        session_id = self.session_id

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        dry_run = self.dry_run

        noise: dict[str, Any] | Unset = UNSET
        if not isinstance(self.noise, Unset):
            noise = self.noise.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if parent is not UNSET:
            field_dict["parent"] = parent
        if name is not UNSET:
            field_dict["name"] = name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if shots is not UNSET:
            field_dict["shots"] = shots
        if backend is not UNSET:
            field_dict["backend"] = backend
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
        from ..models.clone_job_payload_settings import CloneJobPayloadSettings
        from ..models.job_metadata import JobMetadata
        from ..models.noise import Noise
        d = dict(src_dict)
        parent = d.pop("parent", UNSET)

        name = d.pop("name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: JobMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = JobMetadata.from_dict(_metadata)




        shots = d.pop("shots", UNSET)

        backend = d.pop("backend", UNSET)

        session_id = d.pop("session_id", UNSET)

        _settings = d.pop("settings", UNSET)
        settings: CloneJobPayloadSettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = CloneJobPayloadSettings.from_dict(_settings)




        dry_run = d.pop("dry_run", UNSET)

        _noise = d.pop("noise", UNSET)
        noise: Noise | Unset
        if isinstance(_noise,  Unset):
            noise = UNSET
        else:
            noise = Noise.from_dict(_noise)




        clone_job_payload = cls(
            parent=parent,
            name=name,
            metadata=metadata,
            shots=shots,
            backend=backend,
            session_id=session_id,
            settings=settings,
            dry_run=dry_run,
            noise=noise,
        )


        clone_job_payload.additional_properties = d
        return clone_job_payload

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
