"""Pin README copy to runtime constants so doc drift is caught in CI."""

from pathlib import Path

from ionq_core._transport import DEFAULT_MAX_RETRIES, RETRYABLE_STATUS_CODES
from ionq_core.ionq_client import _DEFAULT_TIMEOUT
from ionq_core.polling import _DEFAULT_INTERVAL, _MAX_INTERVAL
from ionq_core.polling import _DEFAULT_TIMEOUT as _POLL_DEFAULT_TIMEOUT

README = (Path(__file__).parent.parent / "README.md").read_text()


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
        assert "1.5x" in README
