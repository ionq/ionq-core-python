# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateSiGate = Literal['si']

GATE_SI_GATE_VALUES: set[GateSiGate] = { 'si',  }

def check_gate_si_gate(value: str) -> GateSiGate:
    if value in GATE_SI_GATE_VALUES:
        return cast(GateSiGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_SI_GATE_VALUES!r}")
