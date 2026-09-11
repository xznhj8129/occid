#!/usr/bin/env python3
"""Regenerate all OCCID compiled artifacts and language bindings."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent
SCHEMA_ROOT = REPO_ROOT / "lib" / "schema"
INTEGER_ID_TYPES = {
    "int",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "IntID",
}


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


def _declared_type(field_spec: object) -> str:
    if isinstance(field_spec, dict):
        type_text = str(field_spec.get("type", ""))
    else:
        type_text = str(field_spec)
    type_text = type_text.split("=", 1)[0].strip()
    while type_text.startswith(("optional ", "const ")):
        type_text = type_text.split(" ", 1)[1].strip()
    return type_text


def _is_integer_id_type(type_text: str) -> bool:
    import generate_pydantic as idl

    try:
        node = idl.TypeParser(type_text).parse()
    except idl.SchemaError:
        return False
    if node.kind == "name":
        return node.name in INTEGER_ID_TYPES
    return node.kind == "semantic" and node.name == "IntID" and len(node.semantic_args) == 1


def _is_integer_id_list(type_text: str) -> bool:
    import generate_pydantic as idl

    try:
        node = idl.TypeParser(type_text).parse()
    except idl.SchemaError:
        return False
    if node.kind != "list" or len(node.args) != 1:
        return False
    item = node.args[0]
    if item.kind == "name":
        return item.name in INTEGER_ID_TYPES
    return item.kind == "semantic" and item.name == "IntID" and len(item.semantic_args) == 1


def validate_identity_field_types() -> None:
    """Enforce OCCID's UID and integer ID naming law."""
    violations: list[str] = []
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for model_name, model_spec in (document.get("models") or {}).items():
            if not isinstance(model_spec, dict):
                raise SystemExit(
                    f"{path}: model {model_name} must be a mapping, not "
                    f"{type(model_spec).__name__} ({model_spec!r}); "
                    "the model declaration may be missing its body"
                )
            for field_name, field_spec in (model_spec.get("fields") or {}).items():
                type_text = _declared_type(field_spec)

                if field_name == "uid" or field_name.endswith("_uid"):
                    if type_text != "UID":
                        violations.append(
                            f"{path}: {model_name}.{field_name} must be UID, not {type_text}; "
                            "strings, protocol identifiers, and local references are not OCCID UIDs"
                        )
                    continue

                if field_name.endswith("_uids"):
                    if type_text != "list[UID]":
                        violations.append(
                            f"{path}: {model_name}.{field_name} must be list[UID], not {type_text}"
                        )
                    continue

                if field_name == "id" or field_name.endswith("_id"):
                    if not _is_integer_id_type(type_text):
                        violations.append(
                            f"{path}: {model_name}.{field_name} must be an integer ID, not {type_text}; "
                            "rename strings and external identifiers as refs, codes, names, addresses, or other truthful values"
                        )
                    continue

                if field_name.endswith("_ids") and not _is_integer_id_list(type_text):
                    violations.append(
                        f"{path}: {model_name}.{field_name} must be a list of integer IDs, not {type_text}; "
                        "use *_uids for UID references or rename non-identity values"
                    )

    if violations:
        raise SystemExit("OCCID identity field violations:\n" + "\n".join(violations))


def run(script: str, *args: str) -> None:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        cwd=REPO_ROOT,
    )
    # Child generators write their own actionable diagnostics.  Preserve that
    # output and exit with the child's status instead of adding a second,
    # unhelpful CalledProcessError traceback from this orchestration script.
    if result.returncode:
        raise SystemExit(result.returncode)


def write_contract_markers() -> None:
    """Write structural markers without importing the install-only package layout.

    During generation, the Python binding exists at repository-root
    ``liboccid/py/``.  It becomes ``occid.schema`` only through setuptools
    package-dir mapping, so importing ``occid.contract`` from a raw checkout
    executes ``occid.__init__`` too early and fails.  ``contract_schema.py`` is
    deliberately package-free, so load that source module directly here.
    """
    path = REPO_ROOT / "occid" / "contract_schema.py"
    spec = importlib.util.spec_from_file_location("_occid_contract_schema", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load OCCID contract schema helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    manifest = module.build_manifest(REPO_ROOT)
    marker = {
        "format": manifest["format"],
        "release": manifest.get("release"),
        "global_hash": manifest["global_hash"],
    }
    marker_text = json.dumps(marker, indent=2, sort_keys=True) + "\n"
    (REPO_ROOT / "occid-contract.json").write_text(marker_text, encoding="utf-8")
    (REPO_ROOT / "occid" / "occid-contract.json").write_text(marker_text, encoding="utf-8")


def main() -> None:
    validate_enum_scalars()
    validate_identity_field_types()

    run("compile_occid.py")
    run("generate_pydantic.py")

    write_contract_markers()

    # TypeScript is a first-class OCCID language binding, generated from the
    # same compiled contract as Python.  Keep it behind this single entry point
    # so consumers never have to remember a second generation command.
    run("generate_typescript.py")


if __name__ == "__main__":
    main()
