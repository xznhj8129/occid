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


def _paths(root: Path, include_modules: bool) -> list[Path]:
    paths = sorted((root / "lib/schema/core").rglob("*.schema.yaml"))
    if include_modules and (root / "lib/schema/modules").exists():
        paths += sorted((root / "lib/schema/modules").rglob("*.schema.yaml"))
    return paths


def _model_ids(root: Path) -> dict[str, int]:
    ids = _read_yaml(root / "lib/model_ids.yaml").get("model_ids")
    if not isinstance(ids, dict):
        raise SchemaContractError("lib/model_ids.yaml lacks model_ids mapping")
    return {str(name): int(value) for name, value in ids.items()}


def _refs(text: str, known: set[str]) -> set[str]:
    return {name for name in _IDENTIFIER.findall(text) if name in known}


def _variant_enum(name: str) -> str:
    return f"{name}_type"


def _snake(name: str) -> str:
    parts: list[str] = []
    current = ""
    for char in name:
        if char.isupper() and current:
            parts.append(current)
            current = char
        else:
            current += char
    if current:
        parts.append(current)
    return "_".join(part.upper() for part in parts)


def _variant_member(parent: str, child: str) -> str:
    p = parent[4:] if parent.startswith("Base") else parent
    c = child[4:] if child.startswith("Base") else child
    if c.startswith(p) and c != p:
        c = c[len(p):]
    elif c.endswith(p) and c != p:
        c = c[:-len(p)]
    return _snake(c)


def build_manifest(repo_root: str | Path, *, include_modules: bool = True) -> dict[str, Any]:
    """Hash the complete canonical OCCID schema graph.

    Each symbol hash includes the full reachable definitions of its parents,
    fields, enums, maps and variants. Any change in that closure cascades into
    every dependent symbol hash.
    """
    root = Path(repo_root).resolve()
    paths = _paths(root, include_modules)
    if not paths:
        raise SchemaContractError(f"no OCCID schema documents under {root / 'lib/schema'}")
    documents = [(path, _read_yaml(path)) for path in paths]
    model_ids = _model_ids(root)
    raw: dict[str, dict[str, Any]] = {}
    variants: dict[str, list[str]] = {}

    def add(name: str, kind: str, definition: Any, source: str) -> None:
        if name in raw:
            raise SchemaContractError(f"duplicate OCCID schema symbol {name}: {source}")
        raw[name] = {"kind": kind, "definition": definition, "source": source}

    for path, doc in documents:
        source = path.relative_to(root).as_posix()
        for name, value in (doc.get("enums") or {}).items():
            add(str(name), "enum", value, source)
        for name, value in (doc.get("maps") or {}).items():
            add(str(name), "map", value, source)
        for name, value in (doc.get("models") or {}).items():
            name = str(name)
            spec = dict(value or {})
            if name not in model_ids:
                raise SchemaContractError(f"model {name} has no permanent ID in lib/model_ids.yaml")
            add(name, "model", {"model_id": model_ids[name], **spec}, source)
            variants[name] = list(spec.get("variants") or [])

    for path, doc in documents:
        for parent, children in (doc.get("extend_variants") or {}).items():
            if parent not in raw or raw[parent]["kind"] != "model":
                raise SchemaContractError(f"extend_variants references unknown model {parent} in {path}")
            variants.setdefault(parent, []).extend(str(child) for child in children)

    for name, children in list(variants.items()):
        if not children:
            continue
        raw[name]["definition"] = {**raw[name]["definition"], "variants": children}
        add(
            _variant_enum(name),
            "variant_enum",
            [{"name": _variant_member(name, child), "model": child} for child in children],
            raw[name]["source"],
        )

    known = set(raw)
    deps: dict[str, set[str]] = {name: set() for name in raw}
    for name, entry in raw.items():
        definition = entry["definition"]
        current = deps[name]
        if entry["kind"] == "model":
            parent = definition.get("parent")
            if parent in known:
                current.add(parent)
            children = definition.get("variants") or []
            current.update(child for child in children if child in known)
            enum_name = _variant_enum(name)
            if children and enum_name in known:
                current.add(enum_name)
            for field in (definition.get("fields") or {}).values():
                text = field if isinstance(field, str) else field.get("type") if isinstance(field, dict) else None
                if isinstance(text, str):
                    current.update(_refs(text, known))
        elif entry["kind"] == "map" and isinstance(definition, dict):
            text = definition.get("type")
            if isinstance(text, str):
                current.update(_refs(text, known))
        elif entry["kind"] == "variant_enum":
            current.update(member["model"] for member in definition if member.get("model") in known)
        current.discard(name)

    local = {name: {"kind": item["kind"], "definition": item["definition"]} for name, item in raw.items()}

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
            "source": raw[name]["source"],
        }
        if raw[name]["kind"] == "model":
            item["model_id"] = raw[name]["definition"]["model_id"]
        symbols[name] = item

    global_input = {
        "documents": {path.relative_to(root).as_posix(): doc for path, doc in documents},
        "model_ids": model_ids,
        "include_modules": include_modules,
    }
    version = root / "VERSION"
    release = version.read_text(encoding="utf-8").strip() if version.exists() else None
    return {"format": 1, "release": release, "global_hash": _sha(global_input), "symbols": symbols}
