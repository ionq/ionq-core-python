# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

QISCircuitGateset = Literal['qis']

QIS_CIRCUIT_GATESET_VALUES: set[QISCircuitGateset] = { 'qis',  }

def check_qis_circuit_gateset(value: str) -> QISCircuitGateset:
    if value in QIS_CIRCUIT_GATESET_VALUES:
        return cast(QISCircuitGateset, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QIS_CIRCUIT_GATESET_VALUES!r}")
