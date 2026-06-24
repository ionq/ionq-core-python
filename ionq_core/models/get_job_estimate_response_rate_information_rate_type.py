# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

GetJobEstimateResponseRateInformationRateType = Literal['2qge', 'qct']

GET_JOB_ESTIMATE_RESPONSE_RATE_INFORMATION_RATE_TYPE_VALUES: set[GetJobEstimateResponseRateInformationRateType] = { '2qge', 'qct',  }

def check_get_job_estimate_response_rate_information_rate_type(value: str) -> GetJobEstimateResponseRateInformationRateType:
    if value in GET_JOB_ESTIMATE_RESPONSE_RATE_INFORMATION_RATE_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_JOB_ESTIMATE_RESPONSE_RATE_INFORMATION_RATE_TYPE_VALUES!r}")
