# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-22

### Added

- Auto-generated Python client from the IonQ OpenAPI v0.4 spec (endpoints, typed models, sync + async)
- `IonQClient` convenience wrapper with API key handling, configurable base URL, and User-Agent
- Retry transport with exponential backoff, idempotency-aware retry, and Retry-After support
- Structured exception hierarchy (`IonQError` -> `APIError` -> `AuthenticationError`, `RateLimitError`, etc.)
- Pagination helpers (`iter_jobs`, `aiter_jobs`, `iter_session_jobs`, `aiter_session_jobs`)
- Job polling helpers (`wait_for_job`, `async_wait_for_job`) with timeout and failure detection
- `SessionManager` for QPU session lifecycle (create, end, status, context manager)
- `ClientExtension` API for downstream SDKs to inject hooks, headers, timeouts, and transport wrappers
- Native gate unitary matrices (`gpi_matrix`, `gpi2_matrix`, `ms_matrix`, `zz_matrix`)
- OpenAPI Overlay for spec workarounds (nullable schemas, missing endpoints, gate fixes)
- 100% test coverage on hand-written code (line + branch) enforced in CI
- CI/CD: lint, type check, tests on Python 3.12-3.14, generated code staleness check, weekly spec drift detection
