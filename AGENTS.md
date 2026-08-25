# AGENTS.md

Instructions for AI agents working in this repository. Humans should read [`CONTRIBUTING.md`](CONTRIBUTING.md) first; this file restates the parts that are easy to violate.

## What this is

`ionq-core` is a typed, sync+async Python REST client for the [IonQ Cloud Platform API](https://api.ionq.co/v0.4). Most of `ionq_core/` is **generated** from `openapi.json` via `openapi-python-client`; a small **hand-written** layer at the package root adds retries, hooks, pagination, polling, sessions, structured exceptions, and native-gate unitaries. Apache-2.0, on PyPI as `ionq-core` (see `pyproject.toml` `[project] version` and `classifiers` for release status). Most end users want a higher-level wrapper (`qiskit-ionq`, `cirq-ionq`, `pennylane-ionq`, CUDA-Q, qbraid); `ionq-core` is the wire-level building block those SDKs sit on.

## Setup

```sh
uv sync                # canonical; uv.lock is committed and CI runs UV_FROZEN=true
uvx pre-commit install
```

`uv` is required for dev workflows; `pip` / `poetry` bypass the lockfile.

## Run

```sh
uv run pytest
uv run ruff check
uv run ruff format --check   # drop --check to apply
uv run ty check ionq_core/
uvx pre-commit run --all-files

# Integration tests hit the real IonQ API. Deselected by default; weekly in CI.
export IONQ_API_KEY=...
uv run pytest -m integration --no-cov
```

`pyproject.toml` is the source of truth for these invocations. Tests treat warnings as errors and use `xfail_strict=True`.

## File boundary - the most important rule

`ionq_core/` has two layers:

- **Generated** - overwritten on every regeneration. Listed in [`.gitattributes`](.gitattributes) (`linguist-generated=true` lines) and mirrored in `pyproject.toml`'s `ruff.extend-exclude` + `coverage.run.omit`; `tests/test_docs_consistency.py` keeps the three lists aligned. Exception: `ionq_core/__init__.py` is in `.gitattributes` only - it renders from [`custom-templates/package_init.py.jinja`](custom-templates/package_init.py.jinja), but the rendered output is still linted and coverage-checked.
- **Hand-written** - everything else under `ionq_core/`. Extend, fix bugs, add tests.

To check whether a file is generated:

```sh
grep -E '^ionq_core/' .gitattributes
```

When you hit a bug in generated code:
- **API surface** (endpoint, schema): upstream spec issue. File a bug; don't patch the file.
- **Local schema fix** (e.g. tightening a type): add an action to `openapi-overlay.yaml` and regenerate.
- **Generator-shape fix**: adjust `openapi-python-client-config.yaml` post-hooks or `custom-templates/`.

## Regenerating the client

Run the block in [`CONTRIBUTING.md`](CONTRIBUTING.md#regenerating-the-client) verbatim; [`generated.yml`](.github/workflows/generated.yml) runs the same invocation on every PR. The spec source is `https://api.ionq.co/v0.4/api-docs` (if that version 404s, find the current one). Commit regenerated files in the same PR as the spec/template/overlay change that produced them.

## Calling generated endpoints

Every endpoint module exposes four callables: `sync`, `sync_detailed`, `asyncio`, `asyncio_detailed`. The `_detailed` variants return `Response[T]` (status + headers + parsed); the others return only the parsed body, or `None` on undocumented status when `raise_on_unexpected_status=False`.

**Path params come first (positional or keyword). `client=`, `body=`, and all query params are keyword-only.**

```python
from ionq_core import IonQClient
from ionq_core.api.characterizations import get_characterization
from ionq_core.api.default import create_job, get_job, get_jobs
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload

client = IonQClient()                                          # reads IONQ_API_KEY
get_job.sync(uuid, client=client)                              # one path param
get_characterization.sync(backend, uuid, client=client)        # multiple path params
get_jobs.sync(client=client, status="completed", limit=10)     # query only
create_job.sync(client=client, body=payload)                   # body only
```

Use `next_=` (trailing underscore) for the cursor pagination kwarg - Python keyword collision. `iter_jobs` / `aiter_jobs` / `iter_session_jobs` / `aiter_session_jobs` page for you.

`UNSET` (sentinel from `ionq_core.types`) means "field omitted"; `None` serializes as JSON `null`. `to_dict()` skips `UNSET` and emits `null` for `None`.

Auth is `apiKey`, **not** `Bearer`: `IonQClient` sets `prefix="apiKey"` and the wire header is `Authorization: apiKey {token}`. Don't change this.

## Hand-written conventions

- Every `.py` carries an SPDX header (`# SPDX-FileCopyrightText: <year> IonQ, Inc.` + `Apache-2.0`); generated files also carry `# @generated`. The year must be **uniform across the whole package** or `tests/test_docs_consistency.py` fails CI. At the year boundary, bump every hand-written file to match; the generator post-hook does the rest.
- Each hand-written module declares its public API in `__all__` at the top; `ionq_core/__init__.py` re-exports those.
- Type-checked by `ty` against Python 3.11. Ruff: `target-version = "py311"`, `line-length = 120`, `select = E, F, I, UP, B, SIM, RUF`.
- 100% branch coverage on hand-written code (`--cov-fail-under=100`); generated paths are in `coverage.run.omit`. New conditional branches need new tests.
- Fixtures and shared helpers live in [`tests/conftest.py`](tests/conftest.py); its clients point at a `test.invalid` base URL derived from `DEFAULT_BASE_URL`. Use them instead of constructing clients ad hoc.
- Mock HTTP with `httpx_mock` from `pytest-httpx`. Don't introduce `responses`, `requests-mock`, or VCR.
- Integration tests are marked `pytest.mark.integration` and live in `tests/integration/`. Use the `track_job` fixture so the autouse `cleanup_jobs` fixture deletes anything you create.
- `gates.py` is intentionally NumPy-free (`cmath`, `math`, nested tuples). Keep it that way.

## Drift sentinels - single edits that fan out

Several values are pinned in multiple files (Python floor, API base URL, the generated-path set, numeric defaults that appear in both code and docstrings). [`tests/test_docs_consistency.py`](tests/test_docs_consistency.py) is the canonical, growing list of these alignments; when it fails, read the failing assertion to find the peers and update every one in the same PR.

## CI

Workflows live in [`.github/workflows/`](.github/workflows/) - `ls` it for the current set; each file's `on:` block documents its own triggers. Non-obvious behavior:

- **`generated.yml`** runs the regenerator on every PR and fails if `git diff ionq_core/` is non-empty. This catches hand-edits to generated files.
- **`integration.yml`** runs on a weekly cron and `workflow_dispatch` only, never per PR, so don't rely on it for fast feedback.
- **`spec-drift.yml`** opens or updates a `spec-drift`-labeled issue when upstream `openapi.json` diverges from the vendored copy.
- **`release.yml`** triggers on `v*` tags only and refuses mismatched tag/version pairs or republishing existing PyPI versions.

New workflows must use the local [`.github/actions/setup-uv`](.github/actions/setup-uv) composite action, not `astral-sh/setup-uv` directly, for consistency with the existing matrix.

## PR and release conventions

- Branch off `main`. CODEOWNERS is `@ionq/developer-tools`.
- PR titles become release-notes lines (`gh release create --generate-notes`). Imperative mood, user-facing, no leading ticket number.
- User-visible changes go under `## [Unreleased]` in `CHANGELOG.md`, in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.
- Release: bump `pyproject.toml` `[project] version`, promote `[Unreleased]` → `[X.Y.Z]` in `CHANGELOG.md`, tag `vX.Y.Z`.

## Things to avoid (and what to do instead)

- **Including IonQ confidential information** in any committed artifact - code, comments, commit messages, branch names, PR titles/bodies, test fixtures, docstrings → scrub before pushing; the repo is public (Apache-2.0 on PyPI) and a leak can't be cleanly undone. Confidential covers proprietary algorithms, trade secrets, internal project codenames, internal file paths, server names, IP addresses, API keys, passwords, non-public experimental data, sensitive customer information, PII, and internal-only comments or documentation.
- **Editing generated files by hand** → fix the spec, the overlay, the post-hooks, or the template, then regenerate. CI's `generated.yml` will catch it otherwise.
- **Adding a dependency with `pip install`** → `uv add <pkg>` (or edit `pyproject.toml` and `uv lock`). Check its license first: MIT, Apache-2.0, BSD-2-Clause, and BSD-3-Clause are pre-approved.
- **`Bearer` token examples / `requests` / `aiohttp`** in docs or tests → the library is `httpx`-only and the auth prefix is `apiKey`.
- **Dropping the SPDX header or `# @generated` marker** on regenerated files → a post-hook adds them, so fix `openapi-python-client-config.yaml` rather than re-adding by hand.
- **Adding NumPy or any new runtime dependency** to `gates.py` → keep it pure-Python.

## Where to look first

- Quick start: [`README.md`](README.md) (Bell-state on the simulator).
- Endpoint inventory: `python -c "import json,sys; s=json.load(open('openapi.json')); [print(m.upper(), p) for p,ms in s['paths'].items() for m in ms if m in 'get post put delete patch']"`
- Hand-written entry points: [`ionq_core/ionq_client.py`](ionq_core/ionq_client.py) (the `IonQClient` factory) and [`ionq_core/extensions.py`](ionq_core/extensions.py) (downstream-SDK API).
- Drift checks: [`tests/test_docs_consistency.py`](tests/test_docs_consistency.py).
- Integration smoke test (full job lifecycle): [`tests/integration/test_simulator_job.py`](tests/integration/test_simulator_job.py).
