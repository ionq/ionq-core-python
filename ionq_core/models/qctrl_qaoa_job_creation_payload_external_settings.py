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






T = TypeVar("T", bound="QctrlQaoaJobCreationPayloadExternalSettings")



@_attrs_define
class QctrlQaoaJobCreationPayloadExternalSettings:
    """
        Attributes:
            api_credentials (str): API Key for your Q-CTRL Account
            external_organization (str | Unset): Optional unique slug for your target Q-CTRL organization
     """

    api_credentials: str
    external_organization: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        api_credentials = self.api_credentials

        external_organization = self.external_organization


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "api_credentials": api_credentials,
        })
        if external_organization is not UNSET:
            field_dict["external_organization"] = external_organization

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_credentials = d.pop("api_credentials")

        external_organization = d.pop("external_organization", UNSET)

        qctrl_qaoa_job_creation_payload_external_settings = cls(
            api_credentials=api_credentials,
            external_organization=external_organization,
        )


        qctrl_qaoa_job_creation_payload_external_settings.additional_properties = d
        return qctrl_qaoa_job_creation_payload_external_settings

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
