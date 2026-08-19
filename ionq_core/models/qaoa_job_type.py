# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QaoaJobType = Literal['qctrl.qaoa.v1']

QAOA_JOB_TYPE_VALUES: set[QaoaJobType] = { 'qctrl.qaoa.v1',  }

def check_qaoa_job_type(value: str) -> QaoaJobType:
    if value in QAOA_JOB_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QAOA_JOB_TYPE_VALUES!r}")
