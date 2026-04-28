# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

NoiseModel = Literal['aria-1', 'aria-2', 'forte-1', 'forte-enterprise-1', 'harmony', 'harmony-1', 'harmony-2', 'ideal']

NOISE_MODEL_VALUES: set[NoiseModel] = { 'aria-1', 'aria-2', 'forte-1', 'forte-enterprise-1', 'harmony', 'harmony-1', 'harmony-2', 'ideal',  }

def check_noise_model(value: str) -> NoiseModel:
    if value in NOISE_MODEL_VALUES:
        return cast(NoiseModel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {NOISE_MODEL_VALUES!r}")
