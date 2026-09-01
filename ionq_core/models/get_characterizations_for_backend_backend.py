# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

GetCharacterizationsForBackendBackend = Literal['qpu.forte-1', 'qpu.forte-enterprise-1']

GET_CHARACTERIZATIONS_FOR_BACKEND_BACKEND_VALUES: set[GetCharacterizationsForBackendBackend] = { 'qpu.forte-1', 'qpu.forte-enterprise-1',  }

def check_get_characterizations_for_backend_backend(value: str) -> GetCharacterizationsForBackendBackend:
    if value in GET_CHARACTERIZATIONS_FOR_BACKEND_BACKEND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_CHARACTERIZATIONS_FOR_BACKEND_BACKEND_VALUES!r}")
