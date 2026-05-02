# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateTGate = Literal['t']

GATE_T_GATE_VALUES: set[GateTGate] = { 't',  }

def check_gate_t_gate(value: str) -> GateTGate:
    if value in GATE_T_GATE_VALUES:
        return cast(GateTGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_T_GATE_VALUES!r}")
