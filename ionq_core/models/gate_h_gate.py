# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateHGate = Literal['h']

GATE_H_GATE_VALUES: set[GateHGate] = { 'h',  }

def check_gate_h_gate(value: str) -> GateHGate:
    if value in GATE_H_GATE_VALUES:
        return cast(GateHGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_H_GATE_VALUES!r}")
