# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""URL path-parameter encoding for the generated endpoint modules, wired in by
a post-generation hook in ``openapi-python-client-config.yaml``."""

from urllib.parse import quote


def quote_path_param(value: object) -> str:
    """Percent-encode ``value`` as a single URL path segment.

    Rejects ``""``, ``"."``, and ``".."``: ``quote`` never encodes dots, so
    those values would survive into the URL verbatim and collapse a fixed path
    segment under RFC 3986 normalization (e.g. ``/sessions/../jobs`` ->
    ``/jobs``, turning a session-scoped request into an account-wide one).

    Raises:
        ValueError: If the value is ``""``, ``"."``, or ``".."``.
    """
    segment = str(value)
    if segment in ("", ".", ".."):
        raise ValueError(f"Invalid URL path parameter {segment!r}: it would escape its path segment")
    return quote(segment, safe="")
