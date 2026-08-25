# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

GetBackendBackend = Literal['qpu.forte-1', 'qpu.forte-enterprise-1']

GET_BACKEND_BACKEND_VALUES: set[GetBackendBackend] = { 'qpu.forte-1', 'qpu.forte-enterprise-1',  }

def check_get_backend_backend(value: str) -> GetBackendBackend:
    if value in GET_BACKEND_BACKEND_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_BACKEND_BACKEND_VALUES!r}")
