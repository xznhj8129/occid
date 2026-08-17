#!/usr/bin/env python3
"""Regenerate OCCID reference outputs and structural fingerprints."""
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

    subprocess.run(
        [sys.executable, str(REPO_ROOT / "generate_pydantic.py"), "--all-modules"],
        cwd=REPO_ROOT,
        check=True,
    )

    # This marker belongs to the OCCID module being generated. Consumer tools
    # use it only through their actually imported OCCID module.
    from occid.contract import write_occid_marker

    write_occid_marker(REPO_ROOT)


if __name__ == "__main__":
    main()
