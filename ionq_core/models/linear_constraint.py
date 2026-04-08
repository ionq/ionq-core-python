from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="LinearConstraint")



@_attrs_define
class LinearConstraint:
    r""" A class to model linear inequality constraints of the form

    .. math::

        A x \leq b.

        Attributes:
            coeffs (list[float]):
            rhs (float):
     """

    coeffs: list[float]
    rhs: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        coeffs = self.coeffs



        rhs = self.rhs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "coeffs": coeffs,
            "rhs": rhs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        coeffs = cast(list[float], d.pop("coeffs"))


        rhs = d.pop("rhs")

        linear_constraint = cls(
            coeffs=coeffs,
            rhs=rhs,
        )


        linear_constraint.additional_properties = d
        return linear_constraint

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
