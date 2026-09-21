# Optional convenience wrappers; scripts/regenerate_models.py is the canonical
# regeneration workflow and works on any OS.

PYTEST_ARGS ?=

.PHONY: lint format typecheck test integration regen sync-spec check-generated

lint:
	uv run ruff check
	uv run ruff format --check

format:
	uv run ruff format

typecheck:
	uv run ty check ionq_core/

test:
	uv run pytest $(PYTEST_ARGS)

integration:
	uv run pytest -m integration --no-cov $(PYTEST_ARGS)

regen:
	uv run --group regen python scripts/regenerate_models.py

sync-spec:
	uv run --group regen python scripts/regenerate_models.py --sync-spec

check-generated: regen
	@if [ -n "$$(git status --porcelain ionq_core/)" ]; then \
		echo "Generated code is out of date: run 'make regen' and commit the results."; \
		git diff ionq_core/; \
		exit 1; \
	fi
