from typing import Literal, cast

Modality = Literal['daily', 'monthly', 'weekly']

MODALITY_VALUES: set[Modality] = { 'daily', 'monthly', 'weekly',  }

def check_modality(value: str) -> Modality:
    if value in MODALITY_VALUES:
        return cast(Modality, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MODALITY_VALUES!r}")
