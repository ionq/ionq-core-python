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






T = TypeVar("T", bound="Noise")



@_attrs_define
class Noise:
    """ 
        Attributes:
            model (str): Available options: `ideal`, `harmony`, `harmony-1`, `harmony-2`, `aria-1`, `aria-2`, `forte-1`,
                `forte-enterprise-1`
            seed (int | Unset):
     """

    model: str
    seed: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        model = self.model

        seed = self.seed


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "model": model,
        })
        if seed is not UNSET:
            field_dict["seed"] = seed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        seed = d.pop("seed", UNSET)

        noise = cls(
            model=model,
            seed=seed,
        )

        return noise
