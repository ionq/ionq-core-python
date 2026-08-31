"""Regenerate the generated client packages from the vendored OpenAPI spec.

Canonical invocation:

    uv run --group regen python scripts/regenerate_models.py [--sync-spec]

Applies openapi-overlay.yaml (when present) to openapi.json, then runs
openapi-python-client with the repo's config and custom templates.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_URL = "https://api.ionq.co/v0.4/api-docs"
SPEC_FILE = REPO_ROOT / "openapi.json"
OVERLAY_FILE = REPO_ROOT / "openapi-overlay.yaml"


def _tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        sys.exit(
            f"error: {name!r} not found on PATH; run via 'uv run --group regen python scripts/regenerate_models.py'"
        )
    return path


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sync-spec",
        action="store_true",
        help=f"download the latest spec from {SPEC_URL} before regenerating",
    )
    args = parser.parse_args()

    if args.sync_spec:
        print(f"fetching {SPEC_URL}")
        with urllib.request.urlopen(SPEC_URL, timeout=60) as response:
            SPEC_FILE.write_bytes(response.read())

    with tempfile.TemporaryDirectory() as tmp_dir:
        patched_spec = Path(tmp_dir) / "patched-spec.json"
        if OVERLAY_FILE.exists():
            _run(
                [
                    _tool("oas-patch"),
                    "overlay",
                    str(SPEC_FILE),
                    str(OVERLAY_FILE),
                    "-o",
                    str(patched_spec),
                ]
            )
        else:
            shutil.copyfile(SPEC_FILE, patched_spec)

        _run(
            [
                _tool("openapi-python-client"),
                "generate",
                "--path",
                str(patched_spec),
                "--meta",
                "none",
                "--config",
                "openapi-python-client-config.yaml",
                "--custom-template-path",
                "custom-templates",
                "--output-path",
                "ionq_core",
                "--overwrite",
            ]
        )


if __name__ == "__main__":
    main()
