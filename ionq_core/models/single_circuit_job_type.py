# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

SingleCircuitJobType = Literal['ionq.circuit.v1', 'ionq.qasm3.v1', 'ionq.qir.v1', 'qctrl.qaoa-circuit.v1']

SINGLE_CIRCUIT_JOB_TYPE_VALUES: set[SingleCircuitJobType] = { 'ionq.circuit.v1', 'ionq.qasm3.v1', 'ionq.qir.v1', 'qctrl.qaoa-circuit.v1',  }

def check_single_circuit_job_type(value: str) -> SingleCircuitJobType:
    if value in SINGLE_CIRCUIT_JOB_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SINGLE_CIRCUIT_JOB_TYPE_VALUES!r}")
