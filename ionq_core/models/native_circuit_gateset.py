# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

NativeCircuitGateset = Literal['native']

NATIVE_CIRCUIT_GATESET_VALUES: set[NativeCircuitGateset] = { 'native',  }

def check_native_circuit_gateset(value: str) -> NativeCircuitGateset:
    if value in NATIVE_CIRCUIT_GATESET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NATIVE_CIRCUIT_GATESET_VALUES!r}")
