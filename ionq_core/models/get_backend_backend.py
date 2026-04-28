# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GetBackendBackend = Literal['qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3']

GET_BACKEND_BACKEND_VALUES: set[GetBackendBackend] = { 'qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3',  }

def check_get_backend_backend(value: str) -> GetBackendBackend:
    if value in GET_BACKEND_BACKEND_VALUES:
        return cast(GetBackendBackend, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_BACKEND_BACKEND_VALUES!r}")
