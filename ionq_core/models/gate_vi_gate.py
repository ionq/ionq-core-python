# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateViGate = Literal['vi']

GATE_VI_GATE_VALUES: set[GateViGate] = { 'vi',  }

def check_gate_vi_gate(value: str) -> GateViGate:
    if value in GATE_VI_GATE_VALUES:
        return cast(GateViGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_VI_GATE_VALUES!r}")
