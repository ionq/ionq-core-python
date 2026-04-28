# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

JobsCanceledResponseStatus = Literal['canceled']

JOBS_CANCELED_RESPONSE_STATUS_VALUES: set[JobsCanceledResponseStatus] = { 'canceled',  }

def check_jobs_canceled_response_status(value: str) -> JobsCanceledResponseStatus:
    if value in JOBS_CANCELED_RESPONSE_STATUS_VALUES:
        return cast(JobsCanceledResponseStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOBS_CANCELED_RESPONSE_STATUS_VALUES!r}")
