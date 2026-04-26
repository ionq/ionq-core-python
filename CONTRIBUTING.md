# Contributing to ionq-core

Thank you for your interest in contributing to the IonQ Python client.

## Development setup

```sh
git clone https://github.com/ionq/ionq-core-python.git
cd ionq-core-python
uv sync
```

## Running checks

```sh
uv run pytest                        # tests
uv run ruff check                    # lint
uv run ruff format --check           # format check
uv run ty check ionq_core/           # type check
```

## Code structure

Most of the code in `ionq_core/` is **auto-generated** from the IonQ OpenAPI specification. Do not edit generated files directly -- they will be overwritten on regeneration.

**Generated (do not edit):**
- `ionq_core/api/` -- endpoint modules
- `ionq_core/models/` -- request/response models
- `ionq_core/client.py`, `errors.py`, `types.py`

**Hand-written (edit freely):**
- `ionq_core/__init__.py` -- public API exports
- `ionq_core/ionq_client.py` -- IonQClient convenience wrapper
- `ionq_core/exceptions.py` -- exception hierarchy
- `ionq_core/extensions.py` -- extension API for downstream SDKs
- `ionq_core/_transport.py` -- retry transport (internal)
- `ionq_core/pagination.py` -- pagination helpers
- `ionq_core/polling.py` -- job polling helpers
- `ionq_core/gates.py` -- native gate matrices
- `ionq_core/session.py` -- session lifecycle manager
- `tests/` -- all tests

## Regenerating the client

```sh
curl -s https://api.ionq.co/v0.4/api-docs -o openapi.json

if [ -f openapi-overlay.yaml ]; then
    uvx oas-patch==0.6.0 overlay openapi.json openapi-overlay.yaml -o /tmp/patched-spec.json
else
    cp openapi.json /tmp/patched-spec.json
fi

uvx openapi-python-client==0.28.3 generate \
    --path /tmp/patched-spec.json \
    --meta none \
    --config openapi-python-client-config.yaml \
    --output-path ionq_core \
    --overwrite
```

## Pull requests

- Keep PRs focused on a single change.
- Add tests for new hand-written code. CI enforces 100% branch coverage on all hand-written code.
- CI must pass before merging (lint, tests, type check, generated code staleness check).
- The generated code staleness check on PRs verifies that `ionq_core/` matches what the generator produces. If it fails, regenerate and commit the result.

## Contributor License Agreement

To receive IonQ's CLA, please contact @mjk or email [opensource@ionq.com](mailto:opensource@ionq.com).

## License

By submitting a pull request, you represent that you have the right to license your
contribution to IonQ and the community, and agree that your contribution is licensed
under the [Apache License, Version 2.0](LICENSE).
