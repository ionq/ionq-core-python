# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

GetCharacterizationBackend = Literal['qpu.forte-1', 'qpu.forte-enterprise-1']

GET_CHARACTERIZATION_BACKEND_VALUES: set[GetCharacterizationBackend] = { 'qpu.forte-1', 'qpu.forte-enterprise-1',  }

def check_get_characterization_backend(value: str) -> GetCharacterizationBackend:
    if value in GET_CHARACTERIZATION_BACKEND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_CHARACTERIZATION_BACKEND_VALUES!r}")
