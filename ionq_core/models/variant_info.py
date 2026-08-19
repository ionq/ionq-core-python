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
  from ..models.variant_results import VariantResults





T = TypeVar("T", bound="VariantInfo")



@_attrs_define
class VariantInfo:
    """ 
        Attributes:
            variant_id (str):
            qubit_map (list[float] | None):
            shots (int):
            results (VariantResults | Unset): Per-variant results object. Each entry is keyed by an artifact format
                identifier; pass the descriptor's `id` to `GET /v0.4/jobs/{id}/artifacts/{artifactId}`
                to download the payload, then validate it against the JSON Schema for its format.
                See the [Results formats](/api-reference/v0.4/schemas/results-formats) page for
                the catalog of valid identifiers.
     """

    variant_id: str
    qubit_map: list[float] | None
    shots: int
    results: VariantResults | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.variant_results import VariantResults
        variant_id = self.variant_id

        qubit_map: list[float] | None
        if isinstance(self.qubit_map, list):
            qubit_map = self.qubit_map


        else:
            qubit_map = self.qubit_map

        shots = self.shots

        results: dict[str, Any] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = self.results.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "variant_id": variant_id,
            "qubit_map": qubit_map,
            "shots": shots,
        })
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.variant_results import VariantResults
        d = dict(src_dict)
        variant_id = d.pop("variant_id")

        def _parse_qubit_map(data: object) -> list[float] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                qubit_map_type_0 = cast(list[float], data)

                return qubit_map_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[float] | None, data)

        qubit_map = _parse_qubit_map(d.pop("qubit_map"))


        shots = d.pop("shots")

        _results = d.pop("results", UNSET)
        results: VariantResults | Unset
        if isinstance(_results,  Unset):
            results = UNSET
        else:
            results = VariantResults.from_dict(_results)




        variant_info = cls(
            variant_id=variant_id,
            qubit_map=qubit_map,
            shots=shots,
            results=results,
        )

        return variant_info

