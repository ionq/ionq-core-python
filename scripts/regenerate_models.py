"""Regenerate the generated client packages from the vendored OpenAPI spec.

Canonical invocation:

    uv run --group regen python scripts/regenerate_models.py [--sync-spec]

Invoking this script as such ensures that the commands in here don't need to
be re-run via uv run.

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


def _get_tool_path(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        invocation_cmd = "uv run --group regen python scripts/regenerate_models.py"
        sys.exit(f"error: {name!r} not found on PATH; run via '{invocation_cmd}'")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sync-spec",
        action="store_true",
        help=f"download the latest spec from {SPEC_URL} before regenerating",
    )
    args = parser.parse_args()

    if args.sync_spec:
        with urllib.request.urlopen(SPEC_URL, timeout=60) as response:
            SPEC_FILE.write_bytes(response.read())

    with tempfile.TemporaryDirectory() as tmp_dir:
        patched_spec = Path(tmp_dir) / "patched-spec.json"
        if OVERLAY_FILE.exists():
            cmd = [_get_tool_path("oas-patch"), "overlay", str(SPEC_FILE), str(OVERLAY_FILE), "-o", str(patched_spec)]
            subprocess.run(cmd, check=True, cwd=REPO_ROOT)
        else:
            shutil.copyfile(SPEC_FILE, patched_spec)

        # fmt: off
        cmd = [
            _get_tool_path("openapi-python-client"), "generate",
            "--path", str(patched_spec),
            "--meta", "none",
            "--config", "openapi-python-client-config.yaml",
            "--custom-template-path", "custom-templates",
            "--output-path", "ionq_core",
            "--overwrite",
        ]
        # fmt: on
        subprocess.run(cmd, check=True, cwd=REPO_ROOT)


if __name__ == "__main__":
    main()
