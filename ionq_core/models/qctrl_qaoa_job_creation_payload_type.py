# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

QctrlQaoaJobCreationPayloadType = Literal['qctrl.qaoa.v1']

QCTRL_QAOA_JOB_CREATION_PAYLOAD_TYPE_VALUES: set[QctrlQaoaJobCreationPayloadType] = { 'qctrl.qaoa.v1',  }

def check_qctrl_qaoa_job_creation_payload_type(value: str) -> QctrlQaoaJobCreationPayloadType:
    if value in QCTRL_QAOA_JOB_CREATION_PAYLOAD_TYPE_VALUES:
        return cast(QctrlQaoaJobCreationPayloadType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QCTRL_QAOA_JOB_CREATION_PAYLOAD_TYPE_VALUES!r}")
