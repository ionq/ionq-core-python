# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateVGate = Literal['v']

GATE_V_GATE_VALUES: set[GateVGate] = { 'v',  }

def check_gate_v_gate(value: str) -> GateVGate:
    if value in GATE_V_GATE_VALUES:
        return cast(GateVGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_V_GATE_VALUES!r}")
