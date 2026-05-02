# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateRyGate = Literal['ry']

GATE_RY_GATE_VALUES: set[GateRyGate] = { 'ry',  }

def check_gate_ry_gate(value: str) -> GateRyGate:
    if value in GATE_RY_GATE_VALUES:
        return cast(GateRyGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_RY_GATE_VALUES!r}")
