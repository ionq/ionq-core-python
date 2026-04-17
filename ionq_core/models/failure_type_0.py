from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.failure_type_0_code import check_failure_type_0_code
from ..models.failure_type_0_code import FailureType0Code
from typing import cast






T = TypeVar("T", bound="FailureType0")



@_attrs_define
class FailureType0:
    """ 
        Attributes:
            code (FailureType0Code):
            message (str):
     """

    code: FailureType0Code
    message: str





    def to_dict(self) -> dict[str, Any]:
        code: str = self.code

        message = self.message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
            "message": message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = check_failure_type_0_code(d.pop("code"))




        message = d.pop("message")

        failure_type_0 = cls(
            code=code,
            message=message,
        )

        return failure_type_0

