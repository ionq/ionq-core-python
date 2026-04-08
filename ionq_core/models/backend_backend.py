from typing import Literal, cast

BackendBackend = Literal['qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3']

BACKEND_BACKEND_VALUES: set[BackendBackend] = { 'qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3',  }

def check_backend_backend(value: str) -> BackendBackend:
    if value in BACKEND_BACKEND_VALUES:
        return cast(BackendBackend, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BACKEND_BACKEND_VALUES!r}")
