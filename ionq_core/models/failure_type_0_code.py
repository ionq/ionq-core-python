from typing import Literal, cast

FailureType0Code = Literal['CompilationError', 'ContractExpiredError', 'DebiasingError', 'InternalError', 'InvalidInput', 'NotEnoughQubits', 'OptimizationError', 'PreflightError', 'QuantumCircuitComplexityError', 'QuantumComputerError', 'QuotaExhaustedError', 'SimulationError', 'SimulationTimeout', 'SystemCancel', 'TooLongPredictedExecutionTime', 'TooManyControls', 'TooManyGates', 'TooManyShots', 'UnknownBillingError', 'UnsupportedGate']

FAILURE_TYPE_0_CODE_VALUES: set[FailureType0Code] = { 'CompilationError', 'ContractExpiredError', 'DebiasingError', 'InternalError', 'InvalidInput', 'NotEnoughQubits', 'OptimizationError', 'PreflightError', 'QuantumCircuitComplexityError', 'QuantumComputerError', 'QuotaExhaustedError', 'SimulationError', 'SimulationTimeout', 'SystemCancel', 'TooLongPredictedExecutionTime', 'TooManyControls', 'TooManyGates', 'TooManyShots', 'UnknownBillingError', 'UnsupportedGate',  }

def check_failure_type_0_code(value: str) -> FailureType0Code:
    if value in FAILURE_TYPE_0_CODE_VALUES:
        return cast(FailureType0Code, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FAILURE_TYPE_0_CODE_VALUES!r}")
