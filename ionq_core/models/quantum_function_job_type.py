# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QuantumFunctionJobType = Literal['quantum-function']

QUANTUM_FUNCTION_JOB_TYPE_VALUES: set[QuantumFunctionJobType] = { 'quantum-function',  }

def check_quantum_function_job_type(value: str) -> QuantumFunctionJobType:
    if value in QUANTUM_FUNCTION_JOB_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUANTUM_FUNCTION_JOB_TYPE_VALUES!r}")
