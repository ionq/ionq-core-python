# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

from typing import Literal, cast

JsonMultiCircuitInputGateset = Literal['native', 'qis']

JSON_MULTI_CIRCUIT_INPUT_GATESET_VALUES: set[JsonMultiCircuitInputGateset] = { 'native', 'qis',  }

def check_json_multi_circuit_input_gateset(value: str) -> JsonMultiCircuitInputGateset:
    if value in JSON_MULTI_CIRCUIT_INPUT_GATESET_VALUES:
        return cast(JsonMultiCircuitInputGateset, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JSON_MULTI_CIRCUIT_INPUT_GATESET_VALUES!r}")
