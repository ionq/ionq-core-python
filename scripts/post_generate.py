"""Post-generation hooks for openapi-python-client (cross-platform).

Invoked via post_hooks in openapi-python-client-config.yaml. Hides
AuthenticatedClient.token from repr and prepends SPDX/@generated headers.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent / "ionq_core"


def main() -> None:
    client_file = PACKAGE_DIR / "client.py"
    client_file.write_text(
        re.sub(
            r"(token: str)$",
            r"\1 = field(repr=False)",
            client_file.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        ),
        encoding="utf-8",
    )

    year = datetime.datetime.now(datetime.UTC).year
    header = f"# SPDX-FileCopyrightText: {year} IonQ, Inc.\n# SPDX-License-Identifier: Apache-2.0\n# @generated\n\n"
    for path in PACKAGE_DIR.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# SPDX-FileCopyrightText"):
            path.write_text(header + text, encoding="utf-8")


if __name__ == "__main__":
    main()
