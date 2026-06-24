# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QctrlQaoaJobInputProblemType = Literal['maxcut']

QCTRL_QAOA_JOB_INPUT_PROBLEM_TYPE_VALUES: set[QctrlQaoaJobInputProblemType] = { 'maxcut',  }

def check_qctrl_qaoa_job_input_problem_type(value: str) -> QctrlQaoaJobInputProblemType:
    if value in QCTRL_QAOA_JOB_INPUT_PROBLEM_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QCTRL_QAOA_JOB_INPUT_PROBLEM_TYPE_VALUES!r}")
