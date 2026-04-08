from typing import Literal, cast

CharacterizationBackend = Literal['qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3']

CHARACTERIZATION_BACKEND_VALUES: set[CharacterizationBackend] = { 'qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'qpu.forte-enterprise-2', 'qpu.forte-enterprise-3',  }

def check_characterization_backend(value: str) -> CharacterizationBackend:
    if value in CHARACTERIZATION_BACKEND_VALUES:
        return cast(CharacterizationBackend, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CHARACTERIZATION_BACKEND_VALUES!r}")
