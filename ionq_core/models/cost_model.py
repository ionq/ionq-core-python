# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

CostModel = Literal['2QGE_operations', 'execution_time', 'QCT', 'quantum_compute_time']

COST_MODEL_VALUES: set[CostModel] = { '2QGE_operations', 'execution_time', 'QCT', 'quantum_compute_time',  }

def check_cost_model(value: str) -> CostModel:
    if value in COST_MODEL_VALUES:
        return cast(CostModel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {COST_MODEL_VALUES!r}")
