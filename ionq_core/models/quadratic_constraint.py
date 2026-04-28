# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="QuadraticConstraint")



@_attrs_define
class QuadraticConstraint:
    r""" A class to model quadratic inequality constraints of the form

    .. math::

        x^T P x + r^T x \leq c.

        Attributes:
            quadratic_coeff (list[list[float]]):
            linear_coeff (list[float]):
            rhs (float):
     """

    quadratic_coeff: list[list[float]]
    linear_coeff: list[float]
    rhs: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        quadratic_coeff = []
        for quadratic_coeff_item_data in self.quadratic_coeff:
            quadratic_coeff_item = quadratic_coeff_item_data


            quadratic_coeff.append(quadratic_coeff_item)



        linear_coeff = self.linear_coeff



        rhs = self.rhs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "quadratic_coeff": quadratic_coeff,
            "linear_coeff": linear_coeff,
            "rhs": rhs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        quadratic_coeff = []
        _quadratic_coeff = d.pop("quadratic_coeff")
        for quadratic_coeff_item_data in (_quadratic_coeff):
            quadratic_coeff_item = cast(list[float], quadratic_coeff_item_data)

            quadratic_coeff.append(quadratic_coeff_item)


        linear_coeff = cast(list[float], d.pop("linear_coeff"))


        rhs = d.pop("rhs")

        quadratic_constraint = cls(
            quadratic_coeff=quadratic_coeff,
            linear_coeff=linear_coeff,
            rhs=rhs,
        )


        quadratic_constraint.additional_properties = d
        return quadratic_constraint

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
