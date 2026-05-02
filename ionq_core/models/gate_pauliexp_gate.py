# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GatePauliexpGate = Literal['pauliexp']

GATE_PAULIEXP_GATE_VALUES: set[GatePauliexpGate] = { 'pauliexp',  }

def check_gate_pauliexp_gate(value: str) -> GatePauliexpGate:
    if value in GATE_PAULIEXP_GATE_VALUES:
        return cast(GatePauliexpGate, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GATE_PAULIEXP_GATE_VALUES!r}")
