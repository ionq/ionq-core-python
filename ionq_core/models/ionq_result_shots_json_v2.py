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

if TYPE_CHECKING:
  from ..models.shot_result import ShotResult





T = TypeVar("T", bound="IonqResultShotsJsonV2")



@_attrs_define
class IonqResultShotsJsonV2:
    """ `ionq.result.shots.json.v2` — Per-shot register outcomes. Each shot
    records measured bit arrays for every named register.

        Example:
            {'shots': [{'registers': {'output_all': [1, 0]}}, {'registers': {'output_all': [0, 1]}}]}

        Attributes:
            shots (list[ShotResult]): Array of shot results, one object per shot.
     """

    shots: list[ShotResult]





    def to_dict(self) -> dict[str, Any]:
        from ..models.shot_result import ShotResult
        shots = []
        for shots_item_data in self.shots:
            shots_item = shots_item_data.to_dict()
            shots.append(shots_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "shots": shots,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shot_result import ShotResult
        d = dict(src_dict)
        shots = []
        _shots = d.pop("shots")
        for shots_item_data in (_shots):
            shots_item = ShotResult.from_dict(shots_item_data)



            shots.append(shots_item)


        ionq_result_shots_json_v2 = cls(
            shots=shots,
        )

        return ionq_result_shots_json_v2
