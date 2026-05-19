# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateXGate = Literal['x']

GATE_X_GATE_VALUES: set[GateXGate] = { 'x',  }

def check_gate_x_gate(value: str) -> GateXGate:
    if value in GATE_X_GATE_VALUES:
        return cast(GateXGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_X_GATE_VALUES!r}")
