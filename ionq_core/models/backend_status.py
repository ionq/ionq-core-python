from typing import Literal, cast

BackendStatus = Literal['available', 'unavailable']

BACKEND_STATUS_VALUES: set[BackendStatus] = { 'available', 'unavailable',  }

def check_backend_status(value: str) -> BackendStatus:
    if value in BACKEND_STATUS_VALUES:
        return cast(BackendStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BACKEND_STATUS_VALUES!r}")
