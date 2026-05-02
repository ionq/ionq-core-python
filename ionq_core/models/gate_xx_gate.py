# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateXXGate = Literal['xx']

GATE_XX_GATE_VALUES: set[GateXXGate] = { 'xx',  }

def check_gate_xx_gate(value: str) -> GateXXGate:
    if value in GATE_XX_GATE_VALUES:
        return cast(GateXXGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_XX_GATE_VALUES!r}")
