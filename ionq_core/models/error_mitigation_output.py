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
  from ..models.aggregations_output import AggregationsOutput
  from ..models.error_mitigation_output_debiasing import ErrorMitigationOutputDebiasing
  from ..models.error_mitigation_output_symmetry_verification_type_0 import ErrorMitigationOutputSymmetryVerificationType0





T = TypeVar("T", bound="ErrorMitigationOutput")



@_attrs_define
class ErrorMitigationOutput:
    """ 
        Attributes:
            debiasing (ErrorMitigationOutputDebiasing | Unset):
            symmetry_verification (ErrorMitigationOutputSymmetryVerificationType0 | None | Unset):
            aggregations (AggregationsOutput | Unset):
     """

    debiasing: ErrorMitigationOutputDebiasing | Unset = UNSET
    symmetry_verification: ErrorMitigationOutputSymmetryVerificationType0 | None | Unset = UNSET
    aggregations: AggregationsOutput | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.aggregations_output import AggregationsOutput
        from ..models.error_mitigation_output_debiasing import ErrorMitigationOutputDebiasing
        from ..models.error_mitigation_output_symmetry_verification_type_0 import ErrorMitigationOutputSymmetryVerificationType0
        debiasing: dict[str, Any] | Unset = UNSET
        if not isinstance(self.debiasing, Unset):
            debiasing = self.debiasing.to_dict()

        symmetry_verification: dict[str, Any] | None | Unset
        if isinstance(self.symmetry_verification, Unset):
            symmetry_verification = UNSET
        elif isinstance(self.symmetry_verification, ErrorMitigationOutputSymmetryVerificationType0):
            symmetry_verification = self.symmetry_verification.to_dict()
        else:
            symmetry_verification = self.symmetry_verification

        aggregations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.aggregations, Unset):
            aggregations = self.aggregations.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if debiasing is not UNSET:
            field_dict["debiasing"] = debiasing
        if symmetry_verification is not UNSET:
            field_dict["symmetry_verification"] = symmetry_verification
        if aggregations is not UNSET:
            field_dict["aggregations"] = aggregations

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregations_output import AggregationsOutput
        from ..models.error_mitigation_output_debiasing import ErrorMitigationOutputDebiasing
        from ..models.error_mitigation_output_symmetry_verification_type_0 import ErrorMitigationOutputSymmetryVerificationType0
        d = dict(src_dict)
        _debiasing = d.pop("debiasing", UNSET)
        debiasing: ErrorMitigationOutputDebiasing | Unset
        if isinstance(_debiasing,  Unset):
            debiasing = UNSET
        else:
            debiasing = ErrorMitigationOutputDebiasing.from_dict(_debiasing)




        def _parse_symmetry_verification(data: object) -> ErrorMitigationOutputSymmetryVerificationType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                symmetry_verification_type_0 = ErrorMitigationOutputSymmetryVerificationType0.from_dict(data)



                return symmetry_verification_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ErrorMitigationOutputSymmetryVerificationType0 | None | Unset, data)

        symmetry_verification = _parse_symmetry_verification(d.pop("symmetry_verification", UNSET))


        _aggregations = d.pop("aggregations", UNSET)
        aggregations: AggregationsOutput | Unset
        if isinstance(_aggregations,  Unset):
            aggregations = UNSET
        else:
            aggregations = AggregationsOutput.from_dict(_aggregations)




        error_mitigation_output = cls(
            debiasing=debiasing,
            symmetry_verification=symmetry_verification,
            aggregations=aggregations,
        )

        return error_mitigation_output
