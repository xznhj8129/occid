#!/usr/bin/env python3
"""Regenerate OCCID reference outputs and schema contract fingerprints."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent
SCHEMA_ROOT = REPO_ROOT / "lib" / "schema"


def validate_enum_scalars() -> None:
    """Fail early when YAML coerces a bare enum token into another scalar type."""
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        text = path.read_text(encoding="utf-8")
        raw = yaml.load(text, Loader=yaml.BaseLoader) or {}
        parsed = yaml.safe_load(text) or {}
        raw_enums = raw.get("enums") or {}
        parsed_enums = parsed.get("enums") or {}

        for enum_name, entries in parsed_enums.items():
            if not isinstance(entries, list):
                continue
            raw_entries = raw_enums.get(enum_name) or []
            for index, entry in enumerate(entries):
                if isinstance(entry, str):
                    continue
                literal = raw_entries[index] if index < len(raw_entries) else repr(entry)
                raise SystemExit(
                    f"{path}: enum {enum_name} entry {literal!r} was parsed as "
                    f"{type(entry).__name__} ({entry!r}); rename the token or make its YAML scalar explicit"
                )


def main() -> None:
    validate_enum_scalars()

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
