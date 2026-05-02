# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateYGate = Literal['y']

GATE_Y_GATE_VALUES: set[GateYGate] = { 'y',  }

def check_gate_y_gate(value: str) -> GateYGate:
    if value in GATE_Y_GATE_VALUES:
        return cast(GateYGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_Y_GATE_VALUES!r}")
