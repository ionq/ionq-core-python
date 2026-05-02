# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GateRxGate = Literal['rx']

GATE_RX_GATE_VALUES: set[GateRxGate] = { 'rx',  }

def check_gate_rx_gate(value: str) -> GateRxGate:
    if value in GATE_RX_GATE_VALUES:
        return cast(GateRxGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_RX_GATE_VALUES!r}")
