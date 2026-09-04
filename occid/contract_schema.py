from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class SchemaContractError(RuntimeError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canon(value).encode("utf-8")).hexdigest()


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SchemaContractError(f"schema document must be a mapping: {path}")
    return data



def _refs(text: str, known: set[str]) -> set[str]:
    return {name for name in _IDENTIFIER.findall(text) if name in known}


def build_manifest(repo_root: str | Path, *, include_modules: bool = True) -> dict[str, Any]:
    """Hash the compiled OCCID runtime contract.

    ``occid.yaml`` is the runtime schema boundary. Authored Concept hierarchy is
    compiler input and therefore does not enter consumer structural hashes unless
    it changes the compiled Type/Representation/Vocabulary output.

    ``include_modules`` is retained for API compatibility; the compiled schema
    already includes all loaded modules.
    """
    del include_modules
    root = Path(repo_root).resolve()
    compiled_path = root / "occid.yaml"
    if not compiled_path.is_file():
        compiled_path = root.parent / "occid.yaml"
    if not compiled_path.is_file():
        raise SchemaContractError(f"missing compiled OCCID schema near {root}")

    document = _read_yaml(compiled_path)
    if document.get("version") != 1 or document.get("type") != "occid":
        raise SchemaContractError(f"invalid compiled OCCID schema: {compiled_path}")

    raw: dict[str, dict[str, Any]] = {}

    def add(name: str, kind: str, definition: Any) -> None:
        if name in raw:
            raise SchemaContractError(f"duplicate OCCID runtime symbol {name}")
        raw[name] = {"kind": kind, "definition": definition, "source": "occid.yaml"}

    for name, spec in (document.get("vocabulary") or {}).items():
        add(str(name), "enum", dict(spec or {}))

    runtime_model_ids: dict[int, str] = {}
    for section, role in (("types", "type"), ("representations", "representation")):
        for name, spec in (document.get(section) or {}).items():
            name = str(name)
            definition = dict(spec or {})
            model_id = definition.get("model_id")
            if type(model_id) is not int or model_id <= 0:
                raise SchemaContractError(f"runtime model {name} has invalid model_id {model_id!r}")
            previous = runtime_model_ids.get(model_id)
            if previous is not None:
                raise SchemaContractError(
                    f"runtime models {previous} and {name} share model_id {model_id}"
                )
            runtime_model_ids[model_id] = name
            add(name, role, definition)

    for name, spec in (document.get("maps") or {}).items():
        add(str(name), "map", dict(spec or {}))

    known = set(raw)
    deps: dict[str, set[str]] = {name: set() for name in raw}
    for name, entry in raw.items():
        definition = entry["definition"]
        current = deps[name]
        if entry["kind"] in {"type", "representation"}:
            model_type = definition.get("type")
            if isinstance(model_type, str):
                current.update(_refs(model_type, known))
            for child in definition.get("children") or []:
                if isinstance(child, str) and child in known:
                    current.add(child)
            for field in (definition.get("fields") or {}).values():
                text = field if isinstance(field, str) else field.get("type") if isinstance(field, dict) else None
                if isinstance(text, str):
                    current.update(_refs(text, known))
        elif entry["kind"] == "map":
            text = definition.get("type")
            if isinstance(text, str):
                current.update(_refs(text, known))
        current.discard(name)

    local = {
        name: {"kind": item["kind"], "definition": item["definition"]}
        for name, item in raw.items()
    }

    def closure(root_name: str) -> list[str]:
        seen: set[str] = set()
        stack = [root_name]
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            stack.extend(sorted(deps[name] - seen, reverse=True))
        return sorted(seen)

    symbols: dict[str, dict[str, Any]] = {}
    for name in sorted(raw):
        reachable = closure(name)
        item: dict[str, Any] = {
            "kind": raw[name]["kind"],
            "hash": _sha({"root": name, "symbols": {dep: local[dep] for dep in reachable}}),
            "dependencies": sorted(deps[name]),
            "source": "occid.yaml",
        }
        if raw[name]["kind"] in {"type", "representation"}:
            item["model_id"] = raw[name]["definition"]["model_id"]
        symbols[name] = item

    global_input = {"occid": document}
    version = root / "VERSION"
    release = version.read_text(encoding="utf-8").strip() if version.exists() else None
    return {"format": 1, "release": release, "global_hash": _sha(global_input), "symbols": symbols}
