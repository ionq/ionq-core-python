import pytest

from ionq_core._url import quote_path_param
from ionq_core.api.backends import get_backend
from ionq_core.api.default import (
    get_job_cost,
    get_session,
    get_session_jobs,
    get_variant_shots,
)


class TestQuotePathParam:
    @pytest.mark.parametrize("value", ["..", ".", ""])
    def test_rejects_segment_escaping_values(self, value):
        with pytest.raises(ValueError, match="path parameter"):
            quote_path_param(value)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("abc-123", "abc-123"),
            ("a.b", "a.b"),  # interior dots are legitimate
            ("...", "..."),  # three dots are not a dot segment
            ("a/../b", "a%2F..%2Fb"),  # slashes cannot smuggle dot segments
            ("..%2F", "..%252F"),  # pre-encoded input is re-encoded, not decoded
            ("café", "caf%C3%A9"),
        ],
    )
    def test_encodes_to_a_single_segment(self, value, expected):
        assert quote_path_param(value) == expected

    def test_non_string_values_are_stringified(self):
        assert quote_path_param(42) == "42"


class TestEndpointPathParamRejection:
    """Traversal-shaped ids must fail before a request is built: quote() leaves "." unencoded, so ".." would
    collapse a fixed path segment under RFC 3986 normalization (CWE-23), e.g. /sessions/../jobs -> /jobs."""

    @pytest.mark.parametrize("bad", ["..", ".", ""])
    def test_session_jobs_rejects(self, auth_client, bad):
        with pytest.raises(ValueError, match="path parameter"):
            get_session_jobs.sync_detailed(bad, client=auth_client)

    @pytest.mark.parametrize("bad", ["..", ".", ""])
    async def test_session_jobs_rejects_async(self, auth_client, bad):
        with pytest.raises(ValueError, match="path parameter"):
            await get_session_jobs.asyncio_detailed(bad, client=auth_client)

    @pytest.mark.parametrize(
        "call",
        [
            lambda c: get_variant_shots.sync_detailed("job-uuid", "..", client=c),
            lambda c: get_session.sync_detailed("..", client=c),
            lambda c: get_job_cost.sync_detailed("..", client=c),
            lambda c: get_backend.sync_detailed("..", client=c),
        ],
    )
    def test_other_endpoints_reject(self, auth_client, call):
        with pytest.raises(ValueError, match="path parameter"):
            call(auth_client)

    def test_fixed_segments_survive_hostile_ids(self):
        kwargs = get_session_jobs._get_kwargs("../jobs")
        assert kwargs["url"] == "/sessions/..%2Fjobs/jobs"
        kwargs = get_variant_shots._get_kwargs("job-1", "v.1")
        assert kwargs["url"] == "/jobs/job-1/variants/v.1/results/shots"
