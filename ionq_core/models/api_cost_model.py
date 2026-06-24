# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

ApiCostModel = Literal['2QGE_operations', 'QCT']

API_COST_MODEL_VALUES: set[ApiCostModel] = { '2QGE_operations', 'QCT',  }

def check_api_cost_model(value: str) -> ApiCostModel:
    if value in API_COST_MODEL_VALUES:
        return cast(ApiCostModel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {API_COST_MODEL_VALUES!r}")
