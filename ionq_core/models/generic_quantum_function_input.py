# Copyright 2026 IonQ, Inc.
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
  from ..models.generic_quantum_function_input_data import GenericQuantumFunctionInputData





T = TypeVar("T", bound="GenericQuantumFunctionInput")



@_attrs_define
class GenericQuantumFunctionInput:
    """ 
        Attributes:
            type_ (str):
            data (GenericQuantumFunctionInputData):
            params (list[float] | Unset):
     """

    type_: str
    data: GenericQuantumFunctionInputData
    params: list[float] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.generic_quantum_function_input_data import GenericQuantumFunctionInputData
        type_ = self.type_

        data = self.data.to_dict()

        params: list[float] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "data": data,
        })
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.generic_quantum_function_input_data import GenericQuantumFunctionInputData
        d = dict(src_dict)
        type_ = d.pop("type")

        data = GenericQuantumFunctionInputData.from_dict(d.pop("data"))




        params = cast(list[float], d.pop("params", UNSET))


        generic_quantum_function_input = cls(
            type_=type_,
            data=data,
            params=params,
        )


        generic_quantum_function_input.additional_properties = d
        return generic_quantum_function_input

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
