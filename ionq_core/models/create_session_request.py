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
  from ..models.session_settings_request import SessionSettingsRequest





T = TypeVar("T", bound="CreateSessionRequest")



@_attrs_define
class CreateSessionRequest:
    """ 
        Attributes:
            backend (str):
            settings (SessionSettingsRequest | Unset):
     """

    backend: str
    settings: SessionSettingsRequest | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.session_settings_request import SessionSettingsRequest
        backend = self.backend

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "backend": backend,
        })
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_settings_request import SessionSettingsRequest
        d = dict(src_dict)
        backend = d.pop("backend")

        _settings = d.pop("settings", UNSET)
        settings: SessionSettingsRequest | Unset
        if isinstance(_settings,  Unset):
            settings = UNSET
        else:
            settings = SessionSettingsRequest.from_dict(_settings)




        create_session_request = cls(
            backend=backend,
            settings=settings,
        )

        return create_session_request
