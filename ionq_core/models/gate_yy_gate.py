# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateYYGate = Literal['yy']

GATE_YY_GATE_VALUES: set[GateYYGate] = { 'yy',  }

def check_gate_yy_gate(value: str) -> GateYYGate:
    if value in GATE_YY_GATE_VALUES:
        return cast(GateYYGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_YY_GATE_VALUES!r}")
