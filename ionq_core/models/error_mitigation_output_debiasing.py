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
  from ..models.variant_info import VariantInfo





T = TypeVar("T", bound="ErrorMitigationOutputDebiasing")



@_attrs_define
class ErrorMitigationOutputDebiasing:
    """ 
        Attributes:
            variants (list[VariantInfo] | Unset):
            aggregation_method (str | Unset):
     """

    variants: list[VariantInfo] | Unset = UNSET
    aggregation_method: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.variant_info import VariantInfo
        variants: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variants, Unset):
            variants = []
            for variants_item_data in self.variants:
                variants_item = variants_item_data.to_dict()
                variants.append(variants_item)



        aggregation_method = self.aggregation_method


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if variants is not UNSET:
            field_dict["variants"] = variants
        if aggregation_method is not UNSET:
            field_dict["aggregation_method"] = aggregation_method

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.variant_info import VariantInfo
        d = dict(src_dict)
        _variants = d.pop("variants", UNSET)
        variants: list[VariantInfo] | Unset = UNSET
        if _variants is not UNSET:
            variants = []
            for variants_item_data in _variants:
                variants_item = VariantInfo.from_dict(variants_item_data)



                variants.append(variants_item)


        aggregation_method = d.pop("aggregation_method", UNSET)

        error_mitigation_output_debiasing = cls(
            variants=variants,
            aggregation_method=aggregation_method,
        )


        error_mitigation_output_debiasing.additional_properties = d
        return error_mitigation_output_debiasing

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
