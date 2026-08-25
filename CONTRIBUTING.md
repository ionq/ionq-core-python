# Contributing to ionq-core

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Report unacceptable behavior to <conduct@ionq.co>.

## Getting help

- **Bug reports and feature requests** -> open an issue using the [bug](.github/ISSUE_TEMPLATE/bug_report.yml) or [feature](.github/ISSUE_TEMPLATE/feature_request.yml) template.
- **Account, billing, or platform questions** -> <https://ionq.com/contact>.
- **Security vulnerabilities** -> see [SECURITY.md](SECURITY.md). Do not open a public issue.

## Proposing changes

Most of `ionq-core` is generated from IonQ's OpenAPI spec and overwritten on every regeneration, so check where your change belongs:

- **API surface changes** (endpoints, parameter names, response shapes) -> these come from the upstream spec, not this repo. Open an issue describing the change you want.
- **Bugs in generated code** -> never edit files marked `linguist-generated=true` in [`.gitattributes`](.gitattributes); file an issue instead.
- **Hand-written extensions, tests, docs, type hints, tooling** -> pull requests welcome.

For non-trivial changes, open an issue first to confirm scope.

## Development setup

This project uses [`uv`](https://docs.astral.sh/uv/). `uv.lock` is canonical and CI runs with `UV_FROZEN=true`.

```sh
git clone https://github.com/ionq/ionq-core-python
cd ionq-core-python
uv sync
uvx pre-commit install
```

The Python floor is `requires-python` in `pyproject.toml`; the tested interpreters are the matrix in [`ci.yml`](.github/workflows/ci.yml).

## Running checks locally

```sh
uv run pytest                    # unit tests
uv run ruff check                # lint
uv run ruff format --check       # format check (drop --check to apply)
uv run ty check ionq_core/       # type check
```

Coverage measures only the hand-written modules. Warnings are errors.

### Integration tests

Tests under `tests/integration/` hit the live IonQ API. They are deselected by default and need an API key:

```sh
export IONQ_API_KEY=...
uv run pytest -m integration --no-cov
```

CI runs them weekly via the [`integration`](.github/workflows/integration.yml) workflow against a gated secret, so most contributions do not need them locally.

## Regenerating the client

To regenerate `ionq_core/api/`, `ionq_core/models/`, and the root-level generated files:

```sh
uv sync --group regen
curl -sf https://api.ionq.co/v0.4/api-docs -o openapi.json
uv run oas-patch overlay openapi.json openapi-overlay.yaml -o /tmp/patched-spec.json
uv run openapi-python-client generate \
    --path /tmp/patched-spec.json \
    --meta none \
    --config openapi-python-client-config.yaml \
    --custom-template-path custom-templates \
    --output-path ionq_core \
    --overwrite
```

Keep it in sync with the [`generated`](.github/workflows/generated.yml) workflow, which runs the same command on every PR. The post-hooks in [`openapi-python-client-config.yaml`](openapi-python-client-config.yaml) normalize the output and apply the security rewrites; each one is commented.

Commit regenerated files with the spec or template change that caused them. [`spec-drift.yml`](.github/workflows/spec-drift.yml) checks weekly and opens an issue if `openapi.json` falls behind upstream.

## Pull request workflow

1. Fork and branch off `main`.
2. Add or update tests for any hand-written code you touch.
3. Run the local checks above and `uvx pre-commit run --all-files`.
4. Open a PR against `main` and fill in the **Summary** and **Test plan** sections.
5. CI must pass: lint, tests across the Python matrix, the generated-code staleness check, `pip-audit`, and `zizmor` when workflow files change. `@ionq/developer-tools` reviews.

Commit messages have no enforced format, but PR titles become release notes via `gh release create --generate-notes`. Write each title as a changelog line: imperative, user-facing, no leading ticket number.

Add user-visible changes to [CHANGELOG.md](CHANGELOG.md) under the next release section, in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

## Contributor License Agreement

Contributions are accepted under the project's [Apache 2.0 license](LICENSE). To receive IonQ's CLA, email <opensource@ionq.co>.
