# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

RateCardEntryUnit = Literal['compute_second', 'gates']

RATE_CARD_ENTRY_UNIT_VALUES: set[RateCardEntryUnit] = { 'compute_second', 'gates',  }

def check_rate_card_entry_unit(value: str) -> RateCardEntryUnit:
    if value in RATE_CARD_ENTRY_UNIT_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RATE_CARD_ENTRY_UNIT_VALUES!r}")
