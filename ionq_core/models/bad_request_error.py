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
  from ..models.request_validation import RequestValidation





T = TypeVar("T", bound="BadRequestError")



@_attrs_define
class BadRequestError:
    """ Error when a bad client request was received.

        Attributes:
            error (str): A short error type descrption.
            message (str): A helpful error message.
            status_code (int): The HTTP status code for this error.
            validation (RequestValidation | Unset): Request validation failure details.
     """

    error: str
    message: str
    status_code: int
    validation: RequestValidation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.request_validation import RequestValidation
        error = self.error

        message = self.message

        status_code = self.status_code

        validation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.validation, Unset):
            validation = self.validation.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
            "message": message,
            "statusCode": status_code,
        })
        if validation is not UNSET:
            field_dict["validation"] = validation

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.request_validation import RequestValidation
        d = dict(src_dict)
        error = d.pop("error")

        message = d.pop("message")

        status_code = d.pop("statusCode")

        _validation = d.pop("validation", UNSET)
        validation: RequestValidation | Unset
        if isinstance(_validation,  Unset):
            validation = UNSET
        else:
            validation = RequestValidation.from_dict(_validation)




        bad_request_error = cls(
            error=error,
            message=message,
            status_code=status_code,
            validation=validation,
        )


        bad_request_error.additional_properties = d
        return bad_request_error

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
