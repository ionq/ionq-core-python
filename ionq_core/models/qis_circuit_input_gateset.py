# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QisCircuitInputGateset = Literal['qis']

QIS_CIRCUIT_INPUT_GATESET_VALUES: set[QisCircuitInputGateset] = { 'qis',  }

def check_qis_circuit_input_gateset(value: str) -> QisCircuitInputGateset:
    if value in QIS_CIRCUIT_INPUT_GATESET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QIS_CIRCUIT_INPUT_GATESET_VALUES!r}")
