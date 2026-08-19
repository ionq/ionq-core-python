# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

QaoaResultsProcessingStatus = Literal['complete', 'max_iteration', 'running']

QAOA_RESULTS_PROCESSING_STATUS_VALUES: set[QaoaResultsProcessingStatus] = { 'complete', 'max_iteration', 'running',  }

def check_qaoa_results_processing_status(value: str) -> QaoaResultsProcessingStatus:
    if value in QAOA_RESULTS_PROCESSING_STATUS_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QAOA_RESULTS_PROCESSING_STATUS_VALUES!r}")
