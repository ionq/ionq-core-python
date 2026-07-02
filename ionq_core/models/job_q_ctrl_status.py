# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

JobQCtrlStatus = Literal['complete', 'max_iteration', 'running']

JOB_Q_CTRL_STATUS_VALUES: set[JobQCtrlStatus] = { 'complete', 'max_iteration', 'running',  }

def check_job_q_ctrl_status(value: str) -> JobQCtrlStatus:
    if value in JOB_Q_CTRL_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_Q_CTRL_STATUS_VALUES!r}")
