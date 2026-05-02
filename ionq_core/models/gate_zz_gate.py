# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateZZGate = Literal['zz']

GATE_ZZ_GATE_VALUES: set[GateZZGate] = { 'zz',  }

def check_gate_zz_gate(value: str) -> GateZZGate:
    if value in GATE_ZZ_GATE_VALUES:
        return cast(GateZZGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_ZZ_GATE_VALUES!r}")
