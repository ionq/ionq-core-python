from typing import Literal, cast

JobBackends = Literal['qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'simulator']

JOB_BACKENDS_VALUES: set[JobBackends] = { 'qpu.aria-1', 'qpu.aria-2', 'qpu.forte-1', 'qpu.forte-enterprise-1', 'simulator',  }

def check_job_backends(value: str) -> JobBackends:
    if value in JOB_BACKENDS_VALUES:
        return cast(JobBackends, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_BACKENDS_VALUES!r}")
