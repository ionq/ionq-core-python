# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

Formats = Literal['ionq.native.v1', 'ionq.result.histogram.json.v1', 'ionq.result.histogram.json.v2', 'ionq.result.probabilities-aggregate.json.v1', 'ionq.result.probabilities.json.v1', 'ionq.result.probabilities.json.v2', 'ionq.result.shots.json.v1', 'ionq.result.shots.json.v2']

FORMATS_VALUES: set[Formats] = { 'ionq.native.v1', 'ionq.result.histogram.json.v1', 'ionq.result.histogram.json.v2', 'ionq.result.probabilities-aggregate.json.v1', 'ionq.result.probabilities.json.v1', 'ionq.result.probabilities.json.v2', 'ionq.result.shots.json.v1', 'ionq.result.shots.json.v2',  }

def check_formats(value: str) -> Formats:
    if value in FORMATS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FORMATS_VALUES!r}")
