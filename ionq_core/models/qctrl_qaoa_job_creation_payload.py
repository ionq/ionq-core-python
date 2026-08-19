# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qctrl_qaoa_job_creation_payload_type import check_qctrl_qaoa_job_creation_payload_type
from ..models.qctrl_qaoa_job_creation_payload_type import QctrlQaoaJobCreationPayloadType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.job_metadata import JobMetadata
  from ..models.qctrl_qaoa_job_creation_payload_external_settings import QctrlQaoaJobCreationPayloadExternalSettings
  from ..models.qctrl_qaoa_job_creation_payload_settings import QctrlQaoaJobCreationPayloadSettings
  from ..models.qctrl_qaoa_job_input import QctrlQaoaJobInput





T = TypeVar("T", bound="QctrlQaoaJobCreationPayload")



@_attrs_define
class QctrlQaoaJobCreationPayload:
    """ Submit a combinatorial optimization job to solve a maxcut problem using Q-CTRL's QAOA Solver. See our QAOA Job guide
    for more information.

        Attributes:
            backend (str): Available options: `simulator`, `qpu.forte-1`, `qpu.forte-enterprise-1`
            type_ (QctrlQaoaJobCreationPayloadType):
            input_ (QctrlQaoaJobInput):
            external_settings (QctrlQaoaJobCreationPayloadExternalSettings):
            name (str | Unset):
            metadata (JobMetadata | Unset):
            shots (int | Unset):  Default: 100.
            session_id (str | Unset):
            settings (QctrlQaoaJobCreationPayloadSettings | Unset):
            dry_run (bool | Unset):
     """

    backend: str
    type_: QctrlQaoaJobCreationPayloadType
    input_: QctrlQaoaJobInput
    external_settings: QctrlQaoaJobCreationPayloadExternalSettings
    name: str | Unset = UNSET
    metadata: JobMetadata | Unset = UNSET
    shots: int | Unset = 100
    session_id: str | Unset = UNSET
    settings: QctrlQaoaJobCreationPayloadSettings | Unset = UNSET
    dry_run: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_metadata import JobMetadata
        from ..models.qctrl_qaoa_job_creation_payload_external_settings import QctrlQaoaJobCreationPayloadExternalSettings
        from ..models.qctrl_qaoa_job_creation_payload_settings import QctrlQaoaJobCreationPayloadSettings
        from ..models.qctrl_qaoa_job_input import QctrlQaoaJobInput
        backend = self.backend

        type_: str = self.type_

        input_ = self.input_.to_dict()

        external_settings = self.external_settings.to_dict()

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


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "backend": backend,
            "type": type_,
            "input": input_,
            "external_settings": external_settings,
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

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_metadata import JobMetadata
        from ..models.qctrl_qaoa_job_creation_payload_external_settings import QctrlQaoaJobCreationPayloadExternalSettings
        from ..models.qctrl_qaoa_job_creation_payload_settings import QctrlQaoaJobCreationPayloadSettings
        from ..models.qctrl_qaoa_job_input import QctrlQaoaJobInput
        d = dict(src_dict)
        backend = d.pop("backend")

        type_ = check_qctrl_qaoa_job_creation_payload_type(d.pop("type"))




        input_ = QctrlQaoaJobInput.from_dict(d.pop("input"))




        external_settings = QctrlQaoaJobCreationPayloadExternalSettings.from_dict(d.pop("external_settings"))




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
        settings: QctrlQaoaJobCreationPayloadSettings | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = QctrlQaoaJobCreationPayloadSettings.from_dict(_settings)




        dry_run = d.pop("dry_run", UNSET)

        qctrl_qaoa_job_creation_payload = cls(
            backend=backend,
            type_=type_,
            input_=input_,
            external_settings=external_settings,
            name=name,
            metadata=metadata,
            shots=shots,
            session_id=session_id,
            settings=settings,
            dry_run=dry_run,
        )


        qctrl_qaoa_job_creation_payload.additional_properties = d
        return qctrl_qaoa_job_creation_payload

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
