# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateSGate = Literal['s']

GATE_S_GATE_VALUES: set[GateSGate] = { 's',  }

def check_gate_s_gate(value: str) -> GateSGate:
    if value in GATE_S_GATE_VALUES:
        return cast(GateSGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_S_GATE_VALUES!r}")
