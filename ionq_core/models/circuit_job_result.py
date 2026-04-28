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
  from ..models.circuit_job_result_histogram import CircuitJobResultHistogram
  from ..models.circuit_job_result_probabilities import CircuitJobResultProbabilities
  from ..models.circuit_job_result_shots import CircuitJobResultShots





T = TypeVar("T", bound="CircuitJobResult")



@_attrs_define
class CircuitJobResult:
    """ 
        Attributes:
            probabilities (CircuitJobResultProbabilities | Unset):
            histogram (CircuitJobResultHistogram | Unset):
            shots (CircuitJobResultShots | Unset):
     """

    probabilities: CircuitJobResultProbabilities | Unset = UNSET
    histogram: CircuitJobResultHistogram | Unset = UNSET
    shots: CircuitJobResultShots | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.circuit_job_result_histogram import CircuitJobResultHistogram
        from ..models.circuit_job_result_probabilities import CircuitJobResultProbabilities
        from ..models.circuit_job_result_shots import CircuitJobResultShots
        probabilities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.probabilities, Unset):
            probabilities = self.probabilities.to_dict()

        histogram: dict[str, Any] | Unset = UNSET
        if not isinstance(self.histogram, Unset):
            histogram = self.histogram.to_dict()

        shots: dict[str, Any] | Unset = UNSET
        if not isinstance(self.shots, Unset):
            shots = self.shots.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if probabilities is not UNSET:
            field_dict["probabilities"] = probabilities
        if histogram is not UNSET:
            field_dict["histogram"] = histogram
        if shots is not UNSET:
            field_dict["shots"] = shots

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_job_result_histogram import CircuitJobResultHistogram
        from ..models.circuit_job_result_probabilities import CircuitJobResultProbabilities
        from ..models.circuit_job_result_shots import CircuitJobResultShots
        d = dict(src_dict)
        _probabilities = d.pop("probabilities", UNSET)
        probabilities: CircuitJobResultProbabilities | Unset
        if isinstance(_probabilities,  Unset):
            probabilities = UNSET
        else:
            probabilities = CircuitJobResultProbabilities.from_dict(_probabilities)




        _histogram = d.pop("histogram", UNSET)
        histogram: CircuitJobResultHistogram | Unset
        if isinstance(_histogram,  Unset):
            histogram = UNSET
        else:
            histogram = CircuitJobResultHistogram.from_dict(_histogram)




        _shots = d.pop("shots", UNSET)
        shots: CircuitJobResultShots | Unset
        if isinstance(_shots,  Unset):
            shots = UNSET
        else:
            shots = CircuitJobResultShots.from_dict(_shots)




        circuit_job_result = cls(
            probabilities=probabilities,
            histogram=histogram,
            shots=shots,
        )

        return circuit_job_result

