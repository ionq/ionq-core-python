# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

JobCanceledResponseStatus = Literal['canceled']

JOB_CANCELED_RESPONSE_STATUS_VALUES: set[JobCanceledResponseStatus] = { 'canceled',  }

def check_job_canceled_response_status(value: str) -> JobCanceledResponseStatus:
    if value in JOB_CANCELED_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_CANCELED_RESPONSE_STATUS_VALUES!r}")
