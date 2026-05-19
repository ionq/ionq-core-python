# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateZGate = Literal['z']

GATE_Z_GATE_VALUES: set[GateZGate] = { 'z',  }

def check_gate_z_gate(value: str) -> GateZGate:
    if value in GATE_Z_GATE_VALUES:
        return cast(GateZGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_Z_GATE_VALUES!r}")
