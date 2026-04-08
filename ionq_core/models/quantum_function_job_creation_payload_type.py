from typing import Literal, cast

QuantumFunctionJobCreationPayloadType = Literal['quantum-function']

QUANTUM_FUNCTION_JOB_CREATION_PAYLOAD_TYPE_VALUES: set[QuantumFunctionJobCreationPayloadType] = { 'quantum-function',  }

def check_quantum_function_job_creation_payload_type(value: str) -> QuantumFunctionJobCreationPayloadType:
    if value in QUANTUM_FUNCTION_JOB_CREATION_PAYLOAD_TYPE_VALUES:
        return cast(QuantumFunctionJobCreationPayloadType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUANTUM_FUNCTION_JOB_CREATION_PAYLOAD_TYPE_VALUES!r}")
