# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QisGate = Literal['cnot', 'h', 'not', 'pauliexp', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'v', 'vi', 'x', 'xx', 'y', 'yy', 'z', 'zz']

QIS_GATE_VALUES: set[QisGate] = { 'cnot', 'h', 'not', 'pauliexp', 'rx', 'ry', 'rz', 's', 'si', 'swap', 't', 'ti', 'v', 'vi', 'x', 'xx', 'y', 'yy', 'z', 'zz',  }

def check_qis_gate(value: str) -> QisGate:
    if value in QIS_GATE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QIS_GATE_VALUES!r}")
