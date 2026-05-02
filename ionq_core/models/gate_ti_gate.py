# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateTiGate = Literal['ti']

GATE_TI_GATE_VALUES: set[GateTiGate] = { 'ti',  }

def check_gate_ti_gate(value: str) -> GateTiGate:
    if value in GATE_TI_GATE_VALUES:
        return cast(GateTiGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_TI_GATE_VALUES!r}")
