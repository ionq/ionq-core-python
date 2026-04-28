"""Pin docs and config against runtime constants and each other to catch drift in CI."""

import json
import re
import tomllib
from pathlib import Path
from urllib.parse import urlparse

import pytest

from ionq_core import exceptions, extensions, polling
from ionq_core._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES
from ionq_core.ionq_client import _AUTH_PREFIX, _DEFAULT_BASE_URL, _DEFAULT_TIMEOUT
from ionq_core.polling import _BACKOFF_FACTOR, _DEFAULT_INTERVAL, _MAX_INTERVAL
from ionq_core.polling import _DEFAULT_TIMEOUT as _POLL_DEFAULT_TIMEOUT

ROOT = Path(__file__).parent.parent
README = (ROOT / "README.md").read_text()
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text())
GITATTRIBUTES = (ROOT / ".gitattributes").read_text()
CONTRIB = (ROOT / "CONTRIBUTING.md").read_text()
GENERATED_WF = (ROOT / ".github" / "workflows" / "generated.yml").read_text()
SPEC_DRIFT_WF = (ROOT / ".github" / "workflows" / "spec-drift.yml").read_text()
SESSION_PY = (ROOT / "ionq_core" / "session.py").read_text()

PACKAGE_DESCRIPTION = "A client library for accessing IonQ Cloud Platform API"
EXAMPLE_BACKEND = "qpu.aria-1"
_BACKEND_PATTERN = re.compile(r'SessionManager\([^)]*?"(qpu\.[^"]+)"')


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
        *(str(c) for c in (429, 500, 502, 503)),
        "520",
        "529",
        f"{DEFAULT_MAX_RETRIES} retries",
        f"{int(_DEFAULT_TIMEOUT.read)} seconds",
        f"{int(_DEFAULT_TIMEOUT.connect)}-second connect",
        f"{int(_DEFAULT_INTERVAL)} second ",
        f"{int(_MAX_INTERVAL)}-second cap",
        f"{int(_POLL_DEFAULT_TIMEOUT)} seconds",
        f"{_BACKOFF_FACTOR}x",
        _DEFAULT_BASE_URL,
        f"Authorization: {_AUTH_PREFIX} ",
    ],
)
def test_readme_mentions_runtime_constant(needle):
    assert needle in README


def test_retryable_status_codes_match_runtime():
    assert frozenset({429, 500, 502, 503, *range(520, 530)}) == RETRYABLE_STATUS_CODES


@pytest.mark.parametrize("name", exceptions.__all__)
def test_readme_lists_exception_class(name):
    assert name in README, f"{name} missing from README exception diagram"


@pytest.mark.parametrize("name", polling.__all__)
def test_readme_lists_polling_name(name):
    assert name in README, f"{name} (from polling.__all__) missing from README"


@pytest.mark.parametrize(
    "needle",
    [
        *(str(c) for c in (429, 500, 502, 503)),
        "520-529",
        f"default of {DEFAULT_MAX_RETRIES}",
        f"default of {int(_DEFAULT_TIMEOUT.read)} seconds",
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


@pytest.mark.parametrize("name,text", [("session.py", SESSION_PY), ("README.md", README)])
def test_session_example_backend_consistent(name, text):
    backends = set(_BACKEND_PATTERN.findall(text))
    assert backends == {EXAMPLE_BACKEND}, f"divergent backends in {name}: {backends}"


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


def test_pyproject_description_canonical():
    assert PYPROJECT["project"]["description"] == PACKAGE_DESCRIPTION


def test_init_module_docstring_canonical():
    import ionq_core

    assert (ionq_core.__doc__ or "").strip() == PACKAGE_DESCRIPTION


def test_readme_tagline_canonical():
    assert PACKAGE_DESCRIPTION in README


def test_ruff_excludes_match_coverage_omits():
    ruff = {_normalize(p) for p in PYPROJECT["tool"]["ruff"]["extend-exclude"]}
    coverage = {_normalize(p) for p in PYPROJECT["tool"]["coverage"]["run"]["omit"]}
    assert ruff == coverage, f"ruff vs coverage divergence: {ruff ^ coverage}"


def test_gitattributes_covers_ruff_paths_plus_init():
    # __init__.py is generated (template-driven) but kept in scope for ruff/coverage
    # because the template is hand-maintained. .gitattributes still marks it generated.
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
    # Pinning to _DEFAULT_BASE_URL means a v0.4 -> v0.5 bump fails this test until
    # CONTRIBUTING and spec-drift.yml are updated too. Otherwise the drift workflow
    # would silently keep curl'ing the stale endpoint.
    spec_path = f"{urlparse(_DEFAULT_BASE_URL).path}/api-docs"
    assert spec_path in CONTRIB
    assert spec_path in SPEC_DRIFT_WF


def test_default_base_url_matches_spec_servers():
    spec = json.loads((ROOT / "openapi.json").read_text())
    assert spec["servers"][0]["url"] == _DEFAULT_BASE_URL


def test_single_spdx_year_across_package():
    """Generated files get the year injected by the openapi-python-client post-hook;
    hand-written files have a static year. After a new-year regen, both sets must
    be bumped together.
    """
    years = set()
    for py in (ROOT / "ionq_core").rglob("*.py"):
        m = re.match(r"# SPDX-FileCopyrightText: (\d{4}) IonQ, Inc\.", py.read_text())
        if m:
            years.add(m.group(1))
    assert len(years) == 1, f"expected exactly one SPDX year, found: {years}"
