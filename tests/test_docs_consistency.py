"""Pin docs and config against runtime constants and each other to catch drift in CI."""

import json
import re
import tomllib
from pathlib import Path
from urllib.parse import urlparse

import pytest

from ionq_core import extensions, polling
from ionq_core._transport import DEFAULT_MAX_RETRIES
from ionq_core.ionq_client import DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from ionq_core.polling import _BACKOFF_FACTOR, _MAX_INTERVAL
from ionq_core.polling import _DEFAULT_TIMEOUT as _POLL_DEFAULT_TIMEOUT

ROOT = Path(__file__).parent.parent
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text())
GITATTRIBUTES = (ROOT / ".gitattributes").read_text()
CONTRIB = (ROOT / "CONTRIBUTING.md").read_text()
GENERATED_WF = (ROOT / ".github" / "workflows" / "generated.yml").read_text()
SPEC_DRIFT_WF = (ROOT / ".github" / "workflows" / "spec-drift.yml").read_text()


def _normalize(path: str) -> str:
    """Strip trailing /* or ** so 'ionq_core/api/*' == 'ionq_core/api/**' == 'ionq_core/api'."""
    path = path.rstrip("/")
    while path.endswith(("/*", "**")):
        path = path[:-2].rstrip("/")
    return path


def _python_floor() -> str:
    m = re.match(r">=(\d+\.\d+)", PYPROJECT["project"]["requires-python"])
    assert m, f"unexpected requires-python: {PYPROJECT['project']['requires-python']!r}"
    return m.group(1)


def _ci_python_versions() -> list[str]:
    ci_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
    m = re.search(r"python-version:\s*\[([^\]]+)\]", ci_text)
    assert m, "CI matrix not found in ci.yml"
    return re.findall(r'"(\d+\.\d+)"', m.group(1))


def _pin(text: str, package: str) -> str:
    m = re.search(rf"{re.escape(package)}==(\S+)", text)
    assert m, f"{package} pin not found"
    return m.group(1)


@pytest.mark.parametrize(
    "needle",
    [
        f"default of {DEFAULT_MAX_RETRIES}",
        f"default of {int(DEFAULT_TIMEOUT.read)} seconds",
    ],
)
def test_client_extension_docstring_pins(needle):
    doc = extensions.ClientExtension.__doc__ or ""
    assert needle in doc, f"{needle!r} missing from ClientExtension docstring"


@pytest.mark.parametrize(
    "fn,needle",
    [
        (polling.wait_for_job, f"{_BACKOFF_FACTOR}x"),
        (polling.wait_for_job, f"{int(_MAX_INTERVAL)} seconds"),
        (polling.wait_for_job, f"Defaults to {int(_POLL_DEFAULT_TIMEOUT)}"),
        (polling.async_wait_for_job, f"Defaults to {int(_POLL_DEFAULT_TIMEOUT)}"),
    ],
)
def test_polling_docstring_pins(fn, needle):
    assert needle in (fn.__doc__ or ""), f"{needle!r} missing from {fn.__name__}"


def test_pyproject_floor_matches_ci_matrix():
    assert _python_floor() == min(_ci_python_versions())


def test_python_version_file_matches_floor():
    assert (ROOT / ".python-version").read_text().strip() == _python_floor()


def test_ruff_target_version_matches_floor():
    floor = _python_floor()
    target = PYPROJECT["tool"]["ruff"]["target-version"]
    assert target == "py" + floor.replace(".", ""), f"ruff target-version {target!r} != floor {floor!r}"


def test_ty_python_version_matches_floor():
    assert PYPROJECT["tool"]["ty"]["environment"]["python-version"] == _python_floor()


def test_classifiers_match_ci_matrix():
    classifiers = sorted(
        c.split("::")[-1].strip()
        for c in PYPROJECT["project"]["classifiers"]
        if c.startswith("Programming Language :: Python :: 3.")
    )
    assert sorted(_ci_python_versions()) == classifiers, f"matrix={_ci_python_versions()} classifiers={classifiers}"


def test_ruff_excludes_match_coverage_omits():
    ruff = {_normalize(p) for p in PYPROJECT["tool"]["ruff"]["extend-exclude"]}
    coverage = {_normalize(p) for p in PYPROJECT["tool"]["coverage"]["run"]["omit"]}
    assert ruff == coverage, f"ruff vs coverage divergence: {ruff ^ coverage}"


def test_gitattributes_covers_ruff_paths_plus_init():
    # __init__.py: hand-edited template, generated output; in ruff/coverage scope, marked linguist-generated.
    gitattr = {
        _normalize(line.split()[0])
        for line in GITATTRIBUTES.splitlines()
        if "linguist-generated=true" in line and line.startswith("ionq_core/")
    }
    ruff = {_normalize(p) for p in PYPROJECT["tool"]["ruff"]["extend-exclude"]}
    assert gitattr == ruff | {"ionq_core/__init__.py"}


def test_openapi_python_client_versions_match():
    assert _pin(CONTRIB, "openapi-python-client") == _pin(GENERATED_WF, "openapi-python-client")


def test_oas_patch_versions_match():
    assert _pin(CONTRIB, "oas-patch") == _pin(GENERATED_WF, "oas-patch")


def test_spec_path_matches_default_base_url():
    # Without this, a DEFAULT_BASE_URL bump leaves spec-drift.yml curling the stale endpoint.
    spec_path = f"{urlparse(DEFAULT_BASE_URL).path}/api-docs"
    assert spec_path in CONTRIB
    assert spec_path in SPEC_DRIFT_WF


def test_spec_servers_path_in_docs():
    # Catches a stale openapi.json: code/docs bumped without regen, or fetched from the wrong version.
    spec = json.loads((ROOT / "openapi.json").read_text())
    spec_path = urlparse(spec["servers"][0]["url"]).path
    assert f"{spec_path}/api-docs" in CONTRIB
    assert f"{spec_path}/api-docs" in SPEC_DRIFT_WF


def test_single_spdx_year_across_package():
    """Generated files get the year via post-hook; hand-written files must be bumped to match at year boundaries."""
    years = set()
    for py in (ROOT / "ionq_core").rglob("*.py"):
        m = re.match(r"# SPDX-FileCopyrightText: (\d{4}) IonQ, Inc\.", py.read_text())
        if m:
            years.add(m.group(1))
    assert len(years) == 1, f"expected exactly one SPDX year, found: {years}"
