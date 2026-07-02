# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

NativeCircuitInputGateset = Literal['native']

NATIVE_CIRCUIT_INPUT_GATESET_VALUES: set[NativeCircuitInputGateset] = { 'native',  }

def check_native_circuit_input_gateset(value: str) -> NativeCircuitInputGateset:
    if value in NATIVE_CIRCUIT_INPUT_GATESET_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NATIVE_CIRCUIT_INPUT_GATESET_VALUES!r}")
