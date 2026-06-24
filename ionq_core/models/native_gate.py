# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

NativeGate = Literal['gpi', 'gpi2', 'ms', 'nop', 'zz']

NATIVE_GATE_VALUES: set[NativeGate] = { 'gpi', 'gpi2', 'ms', 'nop', 'zz',  }

def check_native_gate(value: str) -> NativeGate:
    if value in NATIVE_GATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NATIVE_GATE_VALUES!r}")
