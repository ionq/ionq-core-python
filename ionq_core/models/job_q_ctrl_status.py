# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, cast

JobQCtrlStatus = Literal['complete', 'max_iteration', 'running']

JOB_Q_CTRL_STATUS_VALUES: set[JobQCtrlStatus] = { 'complete', 'max_iteration', 'running',  }

def check_job_q_ctrl_status(value: str) -> JobQCtrlStatus:
    if value in JOB_Q_CTRL_STATUS_VALUES:
        return cast(JobQCtrlStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_Q_CTRL_STATUS_VALUES!r}")
