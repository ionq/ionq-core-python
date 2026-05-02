# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateRzGate = Literal['rz']

GATE_RZ_GATE_VALUES: set[GateRzGate] = { 'rz',  }

def check_gate_rz_gate(value: str) -> GateRzGate:
    if value in GATE_RZ_GATE_VALUES:
        return cast(GateRzGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_RZ_GATE_VALUES!r}")
