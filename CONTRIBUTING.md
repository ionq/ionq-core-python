# Contributing to ionq-core

Thanks for your interest in improving `ionq-core`. This guide covers how to file bugs, propose changes, set up a development environment, regenerate the client, and submit pull requests.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Report unacceptable behavior to <conduct@ionq.co>.

## Getting help

- **Bug reports and feature requests** -> open an issue using the [bug](.github/ISSUE_TEMPLATE/bug_report.yml) or [feature](.github/ISSUE_TEMPLATE/feature_request.yml) template.
- **Account, billing, or platform questions** -> <https://ionq.com/contact>.
- **Security vulnerabilities** -> see [SECURITY.md](SECURITY.md). Do not open a public issue.

If you are looking for a higher-level interface (Qiskit, Cirq, PennyLane, CUDA-Q, qBraid), see the framework SDKs linked from the [README](README.md#looking-for-a-higher-level-interface). `ionq-core` is the low-level HTTP client those SDKs are built on.

## Reporting bugs

When opening a bug report, include:

- A minimal reproduction.
- Expected vs. actual behavior, including any traceback.
- The output of:
  ```sh
  python -c "import ionq_core, sys, platform; print(ionq_core.__version__, sys.version, platform.platform())"
  ```

Incomplete reports may be closed and pointed back to this section.

## Proposing changes

`ionq-core` is generated from IonQ's OpenAPI specification, and most of the package is overwritten on every regeneration. Before opening a pull request, check where your change belongs:

- **API surface changes** (new endpoints, parameter names, response shapes) -> these originate in the upstream OpenAPI spec, not this repo. Open an issue describing the change you want to see.
- **Bugs in generated code** (any file with the `# @generated` marker) -> these originate upstream or in the generator config. File an issue rather than editing the generated output. See [Code structure](#code-structure).
- **Hand-written extensions, tests, docs, type hints, tooling** -> pull requests welcome.

For non-trivial changes, open an issue first to confirm scope before investing significant time.

## Code structure

`ionq_core/` mixes machine-generated and hand-written code. Files that are overwritten on every regeneration carry the `# @generated` marker in their header; never edit them directly:

- `ionq_core/api/**` and `ionq_core/models/**`
- `ionq_core/client.py`, `errors.py`, `types.py`
- `ionq_core/__init__.py` (regenerated from `custom-templates/package_init.py.jinja`)

Everything else under `ionq_core/`, plus `tests/` and `custom-templates/`, is hand-written and accepts pull requests. `openapi.json` is the vendored upstream spec and is refreshed by the regeneration command below.

The PR-time [`generated`](.github/workflows/generated.yml) workflow regenerates the client and fails the build if the result differs from what is committed. The mechanically generated paths (api/, models/, client.py, errors.py, types.py) are also excluded from `ruff` lint, `ty` type checks, and coverage measurement in `pyproject.toml`. `__init__.py` stays in scope because its template is ours to maintain.

## Development setup

This project uses [`uv`](https://docs.astral.sh/uv/) for Python and dependency management; the `uv.lock` file is canonical and CI runs with `UV_FROZEN=true`.

```sh
git clone https://github.com/ionq/ionq-core-python
cd ionq-core-python
uv sync
pre-commit install
```

Python 3.12 or newer is required; the CI matrix is the source of truth for tested interpreters.

## Running checks locally

```sh
uv run pytest                    # unit tests; 100% branch coverage gate on hand-written code
uv run ruff check                # lint
uv run ruff format --check       # format check (drop --check to apply)
uv run ty check ionq_core/       # type check
```

Coverage is measured against the hand-written modules only; the generated surface is excluded. Tests treat warnings as errors.

### Integration tests

Tests under `tests/integration/` hit the live IonQ API. They are excluded by default and require an API key:

```sh
export IONQ_API_KEY=...
uv run pytest -m integration --no-cov
```

CI runs them on a weekly schedule via the [`integration`](.github/workflows/integration.yml) workflow against a gated secret; you do not need to run them locally for most contributions.

## Regenerating the client

To regenerate `ionq_core/api/`, `ionq_core/models/`, and the root-level generated files, run:

```sh
curl -sf https://api.ionq.co/v0.4/api-docs -o openapi.json

if [ -f openapi-overlay.yaml ]; then
    uvx oas-patch==0.6.0 overlay openapi.json openapi-overlay.yaml -o /tmp/patched-spec.json
else
    cp openapi.json /tmp/patched-spec.json
fi

uvx openapi-python-client==0.28.3 generate \
    --path /tmp/patched-spec.json \
    --meta none \
    --config openapi-python-client-config.yaml \
    --custom-template-path custom-templates \
    --output-path ionq_core \
    --overwrite
```

Keep this command in sync with the [`generated`](.github/workflows/generated.yml) workflow, which runs the same invocation on every PR.

Post-generation hooks defined in `openapi-python-client-config.yaml` patch `AuthenticatedClient.token` so API keys do not leak into `repr`, prepend the SPDX and `# @generated` header to every Python file, and run `ruff check --fix-only` followed by `ruff format`.

Commit the regenerated files alongside the spec or template change that caused them. Spec drift is checked weekly by [`spec-drift.yml`](.github/workflows/spec-drift.yml), which opens an issue if `openapi.json` falls behind upstream.

## Pull request workflow

1. Fork the repository and create a topic branch off `main`.
2. Make your changes; add or update tests for any hand-written code you touch.
3. Run the local checks above and `pre-commit run --all-files`.
4. Push and open a PR against `main`. Fill in the **Summary** and **Test plan** sections of the template.
5. CI must pass: lint, tests across the supported-Python matrix, the generated-code staleness check, `pip-audit`, and `zizmor` when workflow files change. A reviewer from `@ionq/developer-tools` will review.

There is no enforced commit-message format, but PR titles become release notes via `gh release create --generate-notes`. Write each title as the line you would want to see in a changelog: imperative mood, user-facing, no leading ticket number.

User-visible changes should also be reflected in [CHANGELOG.md](CHANGELOG.md) under the next release section, in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

## Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) with three carve-outs documented in the [README](README.md#versioning). The SDK version is independent of the IonQ API version.

## Releasing

Maintainers only:

1. Bump `version` in `pyproject.toml`.
2. Add a dated section to `CHANGELOG.md`.
3. Tag the commit `vX.Y.Z` on `main` and push the tag.

The [`release`](.github/workflows/release.yml) workflow verifies that the tag matches `pyproject.toml` and that the version is not already on PyPI, builds with `hatchling`, publishes via PyPI Trusted Publishing (OIDC, no API token), and creates a GitHub Release with auto-generated notes.

## Contributor License Agreement

Contributions are accepted under the project's [Apache 2.0 license](LICENSE). To receive IonQ's CLA, email <opensource@ionq.co>.
