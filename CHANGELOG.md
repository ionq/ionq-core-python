# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `QctrlQaoaJobCreationPayload` and `QctrlQaoaJobInput` for submitting Q-CTRL QAOA maxcut combinatorial-optimization jobs via `create_job`. The `create_job` body union now also accepts `QctrlQaoaJobCreationPayload`.
- `cost_model` optional field on `BaseJob`, `GetCircuitJobResponse`, and `GetJobResponse`, typed as `ApiCostModel` (`"QCT"` or `"2QGE_operations"`).
- `clone_job` endpoint (`POST /jobs/{UUID}/clone`) and its `CloneJobPayload` model for resubmitting an existing job with optional overrides.
- `get_job_artifact` endpoint (`GET /jobs/{UUID}/artifacts/{artifactId}`) for downloading job artifacts by id. The response body is opaque, so only the `sync_detailed` / `asyncio_detailed` callables are generated; read the bytes off `Response.content`.
- `Backend` now exposes `supported_gates`, `supported_native_gates`, and `supported_error_mitigations`.
- `estimate_job_cost` response gained `estimated_quantum_compute_time_us`, and its `rate_information` gained `qct_cost_cents` and `rate_type` (`"qct"` or `"2qge"`). Its `cost_1q_gate`, `cost_2q_gate`, and `job_cost_minimum` rate fields are now nullable.
- `ionq_core.results` module with pure-Python post-processing helpers over the probabilities mapping: `probabilities_to_counts`, `relabel_to_bitstrings`, `marginal`, and `expectation_z`. Keys are little-endian (qubit 0 is the least significant bit).

### Changed

- `NativeCircuitInput.qubits` and `JsonMultiCircuitInput.qubits` are now `int | Unset` (previously `float | Unset`), matching upstream's tightening to `format: int32, minimum: 1`. `QisCircuitInput.qubits` already had this type locally via the OpenAPI overlay; that overlay action has been removed now that upstream is correct natively.
- Regenerated with `openapi-python-client` 0.29.0. Generated models now parse timestamps with the standard library (`datetime.fromisoformat`) instead of `dateutil.parser.isoparse`.

### Removed

- `get_compiled_file` endpoint (`GET /jobs/{UUID}/circuits/{lang}`) and its `GetCompiledFileLang` enum, removed upstream in favor of `get_job_artifact`. Compiled circuits are now fetched as artifacts by id rather than by `lang` (`"native"` / `"qasm3"`).
- `CostModel` model, replaced by `ApiCostModel`.
- The `python-dateutil` runtime dependency, no longer needed now that generated code uses `datetime.fromisoformat`.

## [0.1.1] - 2026-04-30

### Changed

- Lowered minimum supported Python version from 3.12 to 3.11. CI now tests Python 3.11 - 3.14.

## [0.1.0] - 2026-04-29

### Added

- `IonQClient` factory with `IONQ_API_KEY` auto-detection, configurable timeouts, and unified sync + async transports.
- Sync and async variants (`sync`, `sync_detailed`, `asyncio`, `asyncio_detailed`) for every endpoint, generated from the IonQ OpenAPI spec via `openapi-python-client`.
- Endpoint coverage: backends, characterizations, jobs (create, list, get, delete, cancel, cost, estimate, compiled file, probabilities, variant histogram/shots/probabilities), sessions (create, list, get, end, list jobs), usage, whoami.
- Structured exception hierarchy rooted at `IonQError`, with `APIError` subclasses for 400, 401, 403, 404, 429, and 5xx responses, plus `APIConnectionError` and `APITimeoutError` for transport failures. `RateLimitError` exposes `retry_after`.
- Automatic retry with exponential backoff and jitter on 429, 500, 502, 503, and 520-529 (default 2 retries), respecting `Retry-After` headers.
- `ClientExtension` configuration bundle for downstream SDKs: `EventHook` / `AsyncEventHook` protocols, `HookTransport`, custom retryable status codes, header injection, transport wrappers, and `error_mapper`.
- Pagination helpers `iter_jobs`, `aiter_jobs`, `iter_session_jobs`, and `aiter_session_jobs` that auto-follow cursor pagination.
- Polling helpers `wait_for_job` and `async_wait_for_job` with exponential backoff, `JobTimeoutError`, and `JobFailedError`.
- `SessionManager` with sync and async context-manager support, optional `max_jobs` / `max_time` / `max_cost` limits, and `SessionManager.from_id` for reconnecting to existing sessions.
- Native trapped-ion gate unitaries `gpi_matrix`, `gpi2_matrix`, `ms_matrix`, and `zz_matrix` as plain Python nested tuples (no NumPy dependency).
- Typed `attrs` request and response models with `from_dict()` / `to_dict()` and an `Unset` sentinel that distinguishes "not provided" from `None`.
- Python 3.12 - 3.14 support, `py.typed` marker, Apache-2.0 license.

[Unreleased]: https://github.com/ionq/ionq-core-python/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/ionq/ionq-core-python/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ionq/ionq-core-python/releases/tag/v0.1.0
