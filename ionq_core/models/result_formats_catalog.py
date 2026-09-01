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
  from ..models.ionq_result_histogram_json_v1 import IonqResultHistogramJsonV1
  from ..models.ionq_result_histogram_json_v2 import IonqResultHistogramJsonV2
  from ..models.ionq_result_probabilities_aggregate_json_v1 import IonqResultProbabilitiesAggregateJsonV1
  from ..models.ionq_result_probabilities_json_v1 import IonqResultProbabilitiesJsonV1
  from ..models.ionq_result_probabilities_json_v2 import IonqResultProbabilitiesJsonV2
  from ..models.ionq_result_shots_json_v2 import IonqResultShotsJsonV2





T = TypeVar("T", bound="ResultFormatsCatalog")



@_attrs_define
class ResultFormatsCatalog:
    """ Catalog of supported result artifact formats. Each property below documents
    one format's payload structure. Used by the Results formats docs page.

        Attributes:
            ionq_result_probabilities_json_v1 (IonqResultProbabilitiesJsonV1): `ionq.result.probabilities.json.v1` — Legacy
                probability distribution.
                Flat object keyed by decimal qubit state integer strings, values are
                probabilities summing to 1. Example: {'0': 0.5, '1': 0.25, '3': 0.25}.
            ionq_result_probabilities_json_v2 (IonqResultProbabilitiesJsonV2): `ionq.result.probabilities.json.v2` —
                Register-nested probability distribution.
                Each register maps zero-padded bitstrings to probabilities summing to 1 within
                the register. Example: {'probabilities': {'registers': {'output_all': {'11': 0.5, '00': 0.5}}}}.
            ionq_result_histogram_json_v1 (IonqResultHistogramJsonV1): `ionq.result.histogram.json.v1` — Legacy shot count
                histogram.
                Flat object keyed by decimal qubit state integer strings, values are shot counts. Example: {'0': 500, '1': 250,
                '3': 250}.
            ionq_result_histogram_json_v2 (IonqResultHistogramJsonV2): `ionq.result.histogram.json.v2` — Register-nested
                shot count histogram.
                Each register maps zero-padded bitstrings to shot counts. Example: {'histogram': {'registers': {'output_all':
                {'11': 500, '00': 500}}}}.
            ionq_result_shots_json_v1 (list[str]): `ionq.result.shots.json.v1` — Legacy per-shot outcomes.
                Array of decimal qubit state integer strings, one element per shot. Example: ['2', '1', '3', '0'].
            ionq_result_shots_json_v2 (IonqResultShotsJsonV2): `ionq.result.shots.json.v2` — Per-shot register outcomes.
                Each shot
                records measured bit arrays for every named register. Example: {'shots': [{'registers': {'output_all': [1, 0]}},
                {'registers': {'output_all': [0, 1]}}]}.
            ionq_result_probabilities_aggregate_json_v1 (IonqResultProbabilitiesAggregateJsonV1):
                `ionq.result.probabilities-aggregate.json.v1` — Aggregated probability
                distributions across all circuits in an `ionq.multi-circuit.v1` job. Top-level
                keys are child job UUIDs; each value is that child's probability distribution. Example:
                {'06a2099c-f845-7208-8000-8111ee2dccbc': {'2': 1}, '06a2099c-f846-7d32-8000-5726853513db': {'0': 0.5, '1':
                0.5}}.
     """

    ionq_result_probabilities_json_v1: IonqResultProbabilitiesJsonV1
    ionq_result_probabilities_json_v2: IonqResultProbabilitiesJsonV2
    ionq_result_histogram_json_v1: IonqResultHistogramJsonV1
    ionq_result_histogram_json_v2: IonqResultHistogramJsonV2
    ionq_result_shots_json_v1: list[str]
    ionq_result_shots_json_v2: IonqResultShotsJsonV2
    ionq_result_probabilities_aggregate_json_v1: IonqResultProbabilitiesAggregateJsonV1





    def to_dict(self) -> dict[str, Any]:
        from ..models.ionq_result_histogram_json_v1 import IonqResultHistogramJsonV1
        from ..models.ionq_result_histogram_json_v2 import IonqResultHistogramJsonV2
        from ..models.ionq_result_probabilities_aggregate_json_v1 import IonqResultProbabilitiesAggregateJsonV1
        from ..models.ionq_result_probabilities_json_v1 import IonqResultProbabilitiesJsonV1
        from ..models.ionq_result_probabilities_json_v2 import IonqResultProbabilitiesJsonV2
        from ..models.ionq_result_shots_json_v2 import IonqResultShotsJsonV2
        ionq_result_probabilities_json_v1 = self.ionq_result_probabilities_json_v1.to_dict()

        ionq_result_probabilities_json_v2 = self.ionq_result_probabilities_json_v2.to_dict()

        ionq_result_histogram_json_v1 = self.ionq_result_histogram_json_v1.to_dict()

        ionq_result_histogram_json_v2 = self.ionq_result_histogram_json_v2.to_dict()

        ionq_result_shots_json_v1 = self.ionq_result_shots_json_v1



        ionq_result_shots_json_v2 = self.ionq_result_shots_json_v2.to_dict()

        ionq_result_probabilities_aggregate_json_v1 = self.ionq_result_probabilities_aggregate_json_v1.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ionq.result.probabilities.json.v1": ionq_result_probabilities_json_v1,
            "ionq.result.probabilities.json.v2": ionq_result_probabilities_json_v2,
            "ionq.result.histogram.json.v1": ionq_result_histogram_json_v1,
            "ionq.result.histogram.json.v2": ionq_result_histogram_json_v2,
            "ionq.result.shots.json.v1": ionq_result_shots_json_v1,
            "ionq.result.shots.json.v2": ionq_result_shots_json_v2,
            "ionq.result.probabilities-aggregate.json.v1": ionq_result_probabilities_aggregate_json_v1,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ionq_result_histogram_json_v1 import IonqResultHistogramJsonV1
        from ..models.ionq_result_histogram_json_v2 import IonqResultHistogramJsonV2
        from ..models.ionq_result_probabilities_aggregate_json_v1 import IonqResultProbabilitiesAggregateJsonV1
        from ..models.ionq_result_probabilities_json_v1 import IonqResultProbabilitiesJsonV1
        from ..models.ionq_result_probabilities_json_v2 import IonqResultProbabilitiesJsonV2
        from ..models.ionq_result_shots_json_v2 import IonqResultShotsJsonV2
        d = dict(src_dict)
        ionq_result_probabilities_json_v1 = IonqResultProbabilitiesJsonV1.from_dict(d.pop("ionq.result.probabilities.json.v1"))




        ionq_result_probabilities_json_v2 = IonqResultProbabilitiesJsonV2.from_dict(d.pop("ionq.result.probabilities.json.v2"))




        ionq_result_histogram_json_v1 = IonqResultHistogramJsonV1.from_dict(d.pop("ionq.result.histogram.json.v1"))




        ionq_result_histogram_json_v2 = IonqResultHistogramJsonV2.from_dict(d.pop("ionq.result.histogram.json.v2"))




        ionq_result_shots_json_v1 = cast(list[str], d.pop("ionq.result.shots.json.v1"))


        ionq_result_shots_json_v2 = IonqResultShotsJsonV2.from_dict(d.pop("ionq.result.shots.json.v2"))




        ionq_result_probabilities_aggregate_json_v1 = IonqResultProbabilitiesAggregateJsonV1.from_dict(d.pop("ionq.result.probabilities-aggregate.json.v1"))




        result_formats_catalog = cls(
            ionq_result_probabilities_json_v1=ionq_result_probabilities_json_v1,
            ionq_result_probabilities_json_v2=ionq_result_probabilities_json_v2,
            ionq_result_histogram_json_v1=ionq_result_histogram_json_v1,
            ionq_result_histogram_json_v2=ionq_result_histogram_json_v2,
            ionq_result_shots_json_v1=ionq_result_shots_json_v1,
            ionq_result_shots_json_v2=ionq_result_shots_json_v2,
            ionq_result_probabilities_aggregate_json_v1=ionq_result_probabilities_aggregate_json_v1,
        )

        return result_formats_catalog

