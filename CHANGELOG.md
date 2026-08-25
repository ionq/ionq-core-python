# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

- Generated endpoints now reject the path-parameter values `""`, `"."`, and `".."` (raising `ValueError`) before any request is built. `urllib.parse.quote` never encodes dots, so an attacker-supplied identifier like `".."` previously survived into the URL and deleted a fixed path segment under RFC 3986 normalization (e.g. `/sessions/../jobs` -> `/jobs`), redirecting session-scoped reads to account-wide ones.
- `QctrlQaoaJobCreationPayloadExternalSettings.api_credentials` (a Q-CTRL API key) is now excluded from the attrs-generated `repr`, so logging or echoing a job payload can no longer disclose it. `to_dict()` and the wire format are unchanged.
- `AuthenticatedClient` no longer writes the `Authorization` value into its repr-visible, caller-owned headers dict when the httpx clients are built; the credential now lives only on the httpx clients themselves. `repr(client)` stays token-free after use, and a headers dict shared with other clients is no longer contaminated with the key.
- `RateLimitError.retry_after` is now validated by the default transport: values are clamped to at most 300 seconds and non-finite values (`inf`, `nan`, overflowing forms like `1e309`) are treated as absent, so a forged `Retry-After` header cannot drive callers that sleep on it into an unbounded wait or an `OverflowError`.
- The default transport now reads at most 64 KiB (decoded) of an error-response body instead of materializing the whole, transparently decompressed body, preventing memory exhaustion from compression-bomb error responses.
- `verify_ssl` passed to `IonQClient` is now applied to the underlying sync and async httpx transports. Previously the value was silently ignored (httpx disregards client-level `verify` when a custom transport is supplied), so custom CA bundles and pinned `ssl.SSLContext` objects had no effect and `verify_ssl=False` did not actually disable verification.
- The pagination helpers (`iter_jobs`, `aiter_jobs`, `iter_session_jobs`, `aiter_session_jobs`) now raise `IonQError` when the server-supplied `next` cursor is empty or repeats a previously seen cursor, instead of issuing authenticated requests in an unbounded loop.
- The weekly spec-drift workflow fetches the upstream spec from a URL pinned in the workflow instead of one derived from the vendored `openapi.json`, so a tampered spec can no longer point the drift check at a mirror that hides the tampering.

### Added

- `move_job` endpoint (`POST /jobs/{UUID}/move`) and `get_format_schema` endpoint (`GET /schemas/formats/{format}`), from the latest upstream spec.
- Typed per-kind job models returned by `get_job`: `SingleCircuitJob`, `MultiCircuitJob`, `QaoaJob`, and `QuantumFunctionJob`, plus typed result-format models (`IonqResultHistogramJsonV1`/`V2`, `IonqResultProbabilitiesJsonV1`/`V2`, `IonqResultShotsJsonV1`/`V2`, and friends). `QuantumFunctionJobResults` now types `value` and `variance`, which were previously untyped upstream.
- `Matrix2x2` and `Matrix4x4` are now exported from `ionq_core.gates`; they were already documented as the return types of the gate unitaries.
- `QctrlQaoaJobCreationPayload` and `QctrlQaoaJobInput` for submitting Q-CTRL QAOA maxcut combinatorial-optimization jobs via `create_job`. The `create_job` body union now also accepts `QctrlQaoaJobCreationPayload`.
- `cost_model` optional field on `BaseJob`, `GetCircuitJobResponse`, and `GetJobResponse`, typed as `ApiCostModel` (`"QCT"` or `"2QGE_operations"`).
- `clone_job` endpoint (`POST /jobs/{UUID}/clone`) and its `CloneJobPayload` model for resubmitting an existing job with optional overrides.
- `get_job_artifact` endpoint (`GET /jobs/{UUID}/artifacts/{artifactId}`) for downloading job artifacts by id. The response body is opaque, so only the `sync_detailed` / `asyncio_detailed` callables are generated; read the bytes off `Response.content`.
- `Backend` now exposes `supported_gates`, `supported_native_gates`, and `supported_error_mitigations`.
- `estimate_job_cost` response gained `estimated_quantum_compute_time_us`, and its `rate_information` gained `qct_cost_cents` and `rate_type` (`"qct"` or `"2qge"`). Its `cost_1q_gate`, `cost_2q_gate`, and `job_cost_minimum` rate fields are now nullable.

### Changed

- `get_job` (and therefore `wait_for_job` / `async_wait_for_job`) returns `SingleCircuitJob | MultiCircuitJob | QaoaJob | QuantumFunctionJob` instead of the removed `GetJobResponse`.
- The `backend` parameter enum narrowed upstream to `qpu.forte-1` and `qpu.forte-enterprise-1`; `qpu.aria-1`, `qpu.aria-2`, `qpu.forte-enterprise-2`, and `qpu.forte-enterprise-3` are no longer accepted by the typed endpoints that validate it.
- Every `APIError` now carries `retry_after` (parsed and clamped from the `Retry-After` header). Previously only `RateLimitError` exposed it and the value was discarded for other statuses such as 503, where RFC 9110 also allows the header.
- POST requests are no longer retried automatically by the default transport. The API has no idempotency-key mechanism, so replaying `create_job` / `create_session` / `end_session` after an ambiguous gateway 5xx could duplicate billable work; idempotent methods retry as before. Callers that want POST retries must supply their own transport and handle deduplication.
- `NativeCircuitInput.qubits` and `JsonMultiCircuitInput.qubits` are now `int | Unset` (previously `float | Unset`), matching upstream's tightening to `format: int32, minimum: 1`. `QisCircuitInput.qubits` already had this type locally via the OpenAPI overlay; that overlay action has been removed now that upstream is correct natively.
- Regenerated with `openapi-python-client` 0.29.0. Generated models now parse timestamps with the standard library (`datetime.fromisoformat`) instead of `dateutil.parser.isoparse`.

### Fixed

- `IonQClient(headers=...)` no longer raises `TypeError`; caller headers are merged beneath the extension defaults and the generated `User-Agent`.
- `cookies` passed to `IonQClient` now reach the async client as well (previously the sync client only).
- `IonQClient()` no longer builds the TLS trust store twice; the SSL context is created once and shared by the sync and async transports.

### Removed

- Variant-results endpoints (`GET /jobs/{UUID}/variants/{variantId}/results/{shots,histogram,probabilities}`) and their models, removed upstream; per-variant data now arrives through the typed job results and artifacts.
- `GetJobResponse`, `GetCircuitJobResponse`, `GetVariantResultsResponse`, `CircuitJobResult*`, `JsonCircuitInput`, and `NoiseModel` models, restructured upstream into the per-kind job and result-format models above.
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
