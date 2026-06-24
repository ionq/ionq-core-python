# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal

FailureCode = Literal['CompilationError', 'ContractExpiredError', 'DebiasingError', 'InternalError', 'InvalidInput', 'NotEnoughQubits', 'OptimizationError', 'PreflightError', 'QuantumCircuitComplexityError', 'QuantumComputerError', 'QuotaExhaustedError', 'SimulationError', 'SimulationTimeout', 'SystemCancel', 'TooLongPredictedExecutionTime', 'TooManyControls', 'TooManyGates', 'TooManyShots', 'UnknownBillingError', 'UnsupportedGate']

FAILURE_CODE_VALUES: set[FailureCode] = { 'CompilationError', 'ContractExpiredError', 'DebiasingError', 'InternalError', 'InvalidInput', 'NotEnoughQubits', 'OptimizationError', 'PreflightError', 'QuantumCircuitComplexityError', 'QuantumComputerError', 'QuotaExhaustedError', 'SimulationError', 'SimulationTimeout', 'SystemCancel', 'TooLongPredictedExecutionTime', 'TooManyControls', 'TooManyGates', 'TooManyShots', 'UnknownBillingError', 'UnsupportedGate',  }

def check_failure_code(value: str) -> FailureCode:
    if value in FAILURE_CODE_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FAILURE_CODE_VALUES!r}")
