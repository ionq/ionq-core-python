# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateCnotGate = Literal['cnot']

GATE_CNOT_GATE_VALUES: set[GateCnotGate] = { 'cnot',  }

def check_gate_cnot_gate(value: str) -> GateCnotGate:
    if value in GATE_CNOT_GATE_VALUES:
        return cast(GateCnotGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_CNOT_GATE_VALUES!r}")
