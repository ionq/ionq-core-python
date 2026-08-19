# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

MultiCircuitJobType = Literal['ionq.multi-circuit.v1']

MULTI_CIRCUIT_JOB_TYPE_VALUES: set[MultiCircuitJobType] = { 'ionq.multi-circuit.v1',  }

def check_multi_circuit_job_type(value: str) -> MultiCircuitJobType:
    if value in MULTI_CIRCUIT_JOB_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MULTI_CIRCUIT_JOB_TYPE_VALUES!r}")
