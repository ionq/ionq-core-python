# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

ResultFormatHistogramV2 = Literal['ionq.result.histogram.json.v2']

RESULT_FORMAT_HISTOGRAM_V2_VALUES: set[ResultFormatHistogramV2] = { 'ionq.result.histogram.json.v2',  }

def check_result_format_histogram_v2(value: str) -> ResultFormatHistogramV2:
    if value in RESULT_FORMAT_HISTOGRAM_V2_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RESULT_FORMAT_HISTOGRAM_V2_VALUES!r}")
