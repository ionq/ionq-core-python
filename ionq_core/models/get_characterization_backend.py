from typing import Literal, cast

GetCharacterizationBackend = Literal['qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3']

GET_CHARACTERIZATION_BACKEND_VALUES: set[GetCharacterizationBackend] = { 'qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3',  }

def check_get_characterization_backend(value: str) -> GetCharacterizationBackend:
    if value in GET_CHARACTERIZATION_BACKEND_VALUES:
        return cast(GetCharacterizationBackend, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_CHARACTERIZATION_BACKEND_VALUES!r}")
