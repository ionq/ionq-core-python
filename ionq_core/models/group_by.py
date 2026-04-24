# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, cast

GroupBy = Literal['job', 'project', 'user']

GROUP_BY_VALUES: set[GroupBy] = { 'job', 'project', 'user',  }

def check_group_by(value: str) -> GroupBy:
    if value in GROUP_BY_VALUES:
        return cast(GroupBy, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GROUP_BY_VALUES!r}")
