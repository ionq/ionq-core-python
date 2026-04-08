from typing import Literal, cast

JobStatus = Literal['canceled', 'completed', 'failed', 'ready', 'started', 'submitted']

JOB_STATUS_VALUES: set[JobStatus] = { 'canceled', 'completed', 'failed', 'ready', 'started', 'submitted',  }

def check_job_status(value: str) -> JobStatus:
    if value in JOB_STATUS_VALUES:
        return cast(JobStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {JOB_STATUS_VALUES!r}")
