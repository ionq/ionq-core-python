# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateNotGate = Literal['not']

GATE_NOT_GATE_VALUES: set[GateNotGate] = { 'not',  }

def check_gate_not_gate(value: str) -> GateNotGate:
    if value in GATE_NOT_GATE_VALUES:
        return cast(GateNotGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_NOT_GATE_VALUES!r}")
