#!/usr/bin/env python3
"""Regenerate OCCID reference outputs and schema contract fingerprints."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def main() -> None:
    # Preserve the checked-in runtime profile. The Python backend is one output
    # of the schema compiler pipeline; the contract manifest is backend-neutral.
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "generate_pydantic.py"), "--all-modules"],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "-m", "occid.contract", "manifest", str(REPO_ROOT)],
        cwd=REPO_ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
