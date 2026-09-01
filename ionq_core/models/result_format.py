# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

ResultFormat = Literal['ionq.result.histogram.json.v1', 'ionq.result.histogram.json.v2', 'ionq.result.probabilities-aggregate.json.v1', 'ionq.result.probabilities.json.v1', 'ionq.result.probabilities.json.v2', 'ionq.result.shots.json.v1', 'ionq.result.shots.json.v2']

RESULT_FORMAT_VALUES: set[ResultFormat] = { 'ionq.result.histogram.json.v1', 'ionq.result.histogram.json.v2', 'ionq.result.probabilities-aggregate.json.v1', 'ionq.result.probabilities.json.v1', 'ionq.result.probabilities.json.v2', 'ionq.result.shots.json.v1', 'ionq.result.shots.json.v2',  }

def check_result_format(value: str) -> ResultFormat:
    if value in RESULT_FORMAT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RESULT_FORMAT_VALUES!r}")
