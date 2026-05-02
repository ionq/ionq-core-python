# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateSwapGate = Literal['swap']

GATE_SWAP_GATE_VALUES: set[GateSwapGate] = { 'swap',  }

def check_gate_swap_gate(value: str) -> GateSwapGate:
    if value in GATE_SWAP_GATE_VALUES:
        return cast(GateSwapGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_SWAP_GATE_VALUES!r}")
