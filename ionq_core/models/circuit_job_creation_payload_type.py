# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

CircuitJobCreationPayloadType = Literal['ionq.circuit.v1', 'ionq.qasm3.v1']

CIRCUIT_JOB_CREATION_PAYLOAD_TYPE_VALUES: set[CircuitJobCreationPayloadType] = { 'ionq.circuit.v1', 'ionq.qasm3.v1',  }

def check_circuit_job_creation_payload_type(value: str) -> CircuitJobCreationPayloadType:
    if value in CIRCUIT_JOB_CREATION_PAYLOAD_TYPE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CIRCUIT_JOB_CREATION_PAYLOAD_TYPE_VALUES!r}")
