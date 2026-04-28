"""Pin docs and config against runtime constants and each other to catch drift in CI."""

import json
import re
import tomllib
from pathlib import Path
from urllib.parse import urlparse

from ionq_core import exceptions, extensions, polling
from ionq_core._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES, build_transport
from ionq_core.ionq_client import _AUTH_PREFIX, _DEFAULT_BASE_URL, _DEFAULT_TIMEOUT
from ionq_core.polling import _BACKOFF_FACTOR, _DEFAULT_INTERVAL, _MAX_INTERVAL
from ionq_core.polling import _DEFAULT_TIMEOUT as _POLL_DEFAULT_TIMEOUT

ROOT = Path(__file__).parent.parent
README = (ROOT / "README.md").read_text()
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text())
GITATTRIBUTES = (ROOT / ".gitattributes").read_text()


def _normalize(path: str) -> str:
    """Strip trailing /* or ** so 'ionq_core/api/*' == 'ionq_core/api/**' == 'ionq_core/api'."""
    path = path.rstrip("/")
    while path.endswith(("/*", "**")):
        path = path[:-2].rstrip("/")
    return path


class TestREADMEMentionsCurrentConstants:
    def test_retry_status_codes_mentioned(self):
        for code in (429, 500, 502, 503):
            assert str(code) in README
        assert "520" in README and "529" in README
        assert frozenset({429, 500, 502, 503, *range(520, 530)}) == RETRYABLE_STATUS_CODES

    def test_default_max_retries(self):
        assert f"{DEFAULT_MAX_RETRIES} retries" in README

    def test_default_timeout(self):
        assert f"{int(_DEFAULT_TIMEOUT.read)} seconds" in README
        assert f"{int(_DEFAULT_TIMEOUT.connect)}-second connect" in README

    def test_polling_defaults(self):
        assert f"{int(_DEFAULT_INTERVAL)} second " in README
        assert f"{int(_MAX_INTERVAL)}-second cap" in README
        assert f"{int(_POLL_DEFAULT_TIMEOUT)} seconds" in README
        assert f"{_BACKOFF_FACTOR}x" in README

    def test_backoff_parameters(self):
        retry = build_transport()._transport.retry
        assert f"factor {retry.backoff_factor}" in README
        assert f"jitter {retry.backoff_jitter}" in README
        assert f"capped at {int(retry.max_backoff_wait)} seconds" in README

    def test_default_base_url(self):
        assert _DEFAULT_BASE_URL in README

    def test_auth_prefix(self):
        assert f"Authorization: {_AUTH_PREFIX} " in README

    def test_exception_classes_in_diagram(self):
        # Every public exception class in the package must appear in the README hierarchy.
        for name in exceptions.__all__:
            assert name in README, f"{name} missing from README exception diagram"


class TestExtensionDocstringPinsStatusCodes:
    def test_client_extension_lists_retryable_codes(self):
        doc = extensions.ClientExtension.__doc__ or ""
        for code in (429, 500, 502, 503):
            assert str(code) in doc, f"{code} missing from ClientExtension docstring"
        assert "520-529" in doc


class TestSDKExampleBackend:
    """Every QPU backend example in user-facing copy should agree, so a backend
    rename is a single edit instead of a scavenger hunt."""

    EXPECTED = "qpu.aria-1"
    PATTERN = re.compile(r'SessionManager\([^)]*?"(qpu\.[^"]+)"')

    def test_session_module_examples(self):
        text = (ROOT / "ionq_core" / "session.py").read_text()
        backends = set(self.PATTERN.findall(text))
        assert backends == {self.EXPECTED}, f"divergent backends in session.py: {backends}"

    def test_readme_examples(self):
        backends = set(self.PATTERN.findall(README))
        assert backends == {self.EXPECTED}, f"divergent backends in README: {backends}"


class TestPythonFloorConsistency:
    """The lowest Python tested in CI must equal pyproject's floor must equal .python-version."""

    @staticmethod
    def _floor() -> str:
        m = re.match(r">=(\d+\.\d+)", PYPROJECT["project"]["requires-python"])
        assert m, f"unexpected requires-python: {PYPROJECT['project']['requires-python']!r}"
        return m.group(1)

    def test_pyproject_floor_matches_ci_matrix(self):
        ci_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
        m = re.search(r"python-version:\s*\[([^\]]+)\]", ci_text)
        assert m, "CI matrix not found in ci.yml"
        versions = re.findall(r'"(\d+\.\d+)"', m.group(1))
        assert self._floor() == min(versions)

    def test_python_version_file_matches_floor(self):
        assert (ROOT / ".python-version").read_text().strip() == self._floor()

    def test_ruff_target_version_matches_floor(self):
        floor = self._floor()
        target = PYPROJECT["tool"]["ruff"]["target-version"]
        assert target == "py" + floor.replace(".", ""), f"ruff target-version {target!r} != floor {floor!r}"

    def test_ty_python_version_matches_floor(self):
        assert PYPROJECT["tool"]["ty"]["environment"]["python-version"] == self._floor()


class TestPackageDescriptionIsCanonical:
    """pyproject, __init__.py, and README must agree on the package description."""

    EXPECTED = "A client library for accessing IonQ Cloud Platform API"

    def test_pyproject_description(self):
        assert PYPROJECT["project"]["description"] == self.EXPECTED

    def test_init_module_docstring(self):
        import ionq_core

        assert (ionq_core.__doc__ or "").strip() == self.EXPECTED

    def test_readme_tagline(self):
        assert self.EXPECTED in README


class TestGeneratedPathsConsistency:
    """ruff exclude, coverage omit, and .gitattributes must agree on which paths are generated."""

    def test_ruff_excludes_match_coverage_omits(self):
        ruff = {_normalize(p) for p in PYPROJECT["tool"]["ruff"]["extend-exclude"]}
        coverage = {_normalize(p) for p in PYPROJECT["tool"]["coverage"]["run"]["omit"]}
        assert ruff == coverage, f"ruff vs coverage divergence: {ruff ^ coverage}"

    def test_gitattributes_covers_ruff_paths_plus_init(self):
        # __init__.py is generated (template-driven) but kept in scope for ruff/coverage
        # because the template is hand-maintained. .gitattributes still marks it generated.
        gitattr = {
            _normalize(line.split()[0])
            for line in GITATTRIBUTES.splitlines()
            if "linguist-generated=true" in line and line.startswith("ionq_core/")
        }
        ruff = {_normalize(p) for p in PYPROJECT["tool"]["ruff"]["extend-exclude"]}
        assert gitattr == ruff | {"ionq_core/__init__.py"}


class TestGeneratorVersionPins:
    """CONTRIBUTING.md and the generated.yml workflow must pin identical tool versions."""

    CONTRIB = (ROOT / "CONTRIBUTING.md").read_text()
    GENERATED_WF = (ROOT / ".github" / "workflows" / "generated.yml").read_text()
    SPEC_DRIFT_WF = (ROOT / ".github" / "workflows" / "spec-drift.yml").read_text()

    @staticmethod
    def _pin(text: str, package: str) -> str:
        m = re.search(rf"{re.escape(package)}==(\S+)", text)
        assert m, f"{package} pin not found"
        return m.group(1)

    def test_openapi_python_client_versions_match(self):
        assert self._pin(self.CONTRIB, "openapi-python-client") == self._pin(self.GENERATED_WF, "openapi-python-client")

    def test_oas_patch_versions_match(self):
        assert self._pin(self.CONTRIB, "oas-patch") == self._pin(self.GENERATED_WF, "oas-patch")

    def test_spec_path_matches_default_base_url(self):
        # Pinning to _DEFAULT_BASE_URL means a v0.4 -> v0.5 bump fails this test until
        # CONTRIBUTING and spec-drift.yml are updated too. Otherwise the drift workflow
        # would silently keep curl'ing the stale endpoint.
        spec_path = f"{urlparse(_DEFAULT_BASE_URL).path}/api-docs"
        assert spec_path in self.CONTRIB
        assert spec_path in self.SPEC_DRIFT_WF


class TestExtensionDocstringPinsDefaults:
    """ClientExtension docstring numeric defaults must track the runtime constants."""

    def test_max_retries_default_pinned(self):
        doc = extensions.ClientExtension.__doc__ or ""
        assert f"default of {DEFAULT_MAX_RETRIES}" in doc

    def test_timeout_default_pinned(self):
        doc = extensions.ClientExtension.__doc__ or ""
        assert f"default of {int(_DEFAULT_TIMEOUT.read)} seconds" in doc


class TestPollingDocstringPinsConstants:
    """wait_for_job / async_wait_for_job docstrings must reference module constants."""

    def test_sync_pins_backoff_factor(self):
        assert f"{_BACKOFF_FACTOR}x" in (polling.wait_for_job.__doc__ or "")

    def test_sync_pins_max_interval(self):
        assert f"{int(_MAX_INTERVAL)} seconds" in (polling.wait_for_job.__doc__ or "")

    def test_sync_pins_default_timeout(self):
        assert f"Defaults to {int(_POLL_DEFAULT_TIMEOUT)}" in (polling.wait_for_job.__doc__ or "")

    def test_async_pins_default_timeout(self):
        assert f"Defaults to {int(_POLL_DEFAULT_TIMEOUT)}" in (polling.async_wait_for_job.__doc__ or "")


class TestPollingPublicNamesInReadme:
    """Every name in polling.__all__ must appear in the README."""

    def test_each_name_present(self):
        for name in polling.__all__:
            assert name in README, f"{name} (from polling.__all__) missing from README"


class TestClassifiersMatchCIMatrix:
    """pyproject Python classifiers must enumerate exactly the CI Python matrix."""

    def test_classifiers_match_matrix(self):
        ci_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
        m = re.search(r"python-version:\s*\[([^\]]+)\]", ci_text)
        assert m, "CI matrix not found in ci.yml"
        ci_versions = sorted(re.findall(r'"(\d+\.\d+)"', m.group(1)))
        classifiers = sorted(
            c.split("::")[-1].strip()
            for c in PYPROJECT["project"]["classifiers"]
            if c.startswith("Programming Language :: Python :: 3.")
        )
        assert ci_versions == classifiers, f"matrix={ci_versions} classifiers={classifiers}"


class TestDefaultBaseURLMatchesSpec:
    """_DEFAULT_BASE_URL must match the OpenAPI spec's primary server URL."""

    def test_base_url_matches_spec_servers(self):
        spec = json.loads((ROOT / "openapi.json").read_text())
        assert spec["servers"][0]["url"] == _DEFAULT_BASE_URL


class TestSPDXYearConsistency:
    """All SPDX-FileCopyrightText years across ionq_core/ must agree.

    Generated files get the year injected by the openapi-python-client post-hook;
    hand-written files have a static year. After a new-year regen, both sets
    must be bumped together.
    """

    def test_single_year_across_package(self):
        years = set()
        for py in (ROOT / "ionq_core").rglob("*.py"):
            m = re.match(r"# SPDX-FileCopyrightText: (\d{4}) IonQ, Inc\.", py.read_text())
            if m:
                years.add(m.group(1))
        assert len(years) <= 1, f"divergent SPDX years: {years}"


class TestDocAnchorsResolve:
    """Cross-doc anchor links must resolve to actual headings.

    Add a (target_md, anchor) pair when introducing a new link from
    issue/PR templates, README, or CONTRIBUTING that uses an in-page anchor.
    """

    REFS = [
        ("README.md", "looking-for-a-higher-level-interface"),
        ("README.md", "versioning"),
        ("CONTRIBUTING.md", "code-structure"),
        ("CONTRIBUTING.md", "reporting-bugs"),
        ("CONTRIBUTING.md", "proposing-changes"),
    ]

    @staticmethod
    def _slugify(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^\w\s-]", "", s)
        return re.sub(r"\s+", "-", s)

    @classmethod
    def _headings(cls, path: Path) -> set[str]:
        text = path.read_text()
        return {cls._slugify(m.group(1)) for m in re.finditer(r"^#+\s+(.+?)\s*$", text, flags=re.MULTILINE)}

    def test_all_anchors_resolve(self):
        for target, anchor in self.REFS:
            headings = self._headings(ROOT / target)
            assert anchor in headings, f"#{anchor} not found in {target}; have {sorted(headings)}"
