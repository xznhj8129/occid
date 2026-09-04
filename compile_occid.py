#!/usr/bin/env python3
"""Compile authored OCCID semantics into the flat runtime schema ``occid.yaml``.

Authored levels:
    Concept         authored semantic category
    Representation  explicit data-bearing shape
    Vocabulary      enum

Derived level:
    Type            Concept with no Concept children

The compiled runtime schema contains only Types, Representations, Vocabulary,
and constant maps. Runtime inheritance, full Concept ancestry, and variants are
consumed by this compiler and do not survive into ``occid.yaml``. Each emitted
model retains only its nearest ancestor Concept as ``family``.
"""

from __future__ import annotations

import argparse
import copy
from collections import defaultdict
from pathlib import Path

import yaml

import generate_pydantic as idl


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = REPO_ROOT / "occid.yaml"


class CompileError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema-dir", type=Path, default=idl.SCHEMA_DIR)
    parser.add_argument("--module-dir", type=Path, default=idl.MODULE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def render_type(node: idl.TypeNode) -> str:
    if node.kind == "fixed_bytes":
        assert node.size is not None
        return f"bytes[{node.size}]"
    if node.kind == "name":
        assert node.name is not None
        return node.name
    if node.kind == "semantic":
        assert node.name is not None
        return f"{node.name}({', '.join(node.semantic_args)})"
    if node.kind == "list":
        return f"list[{render_type(node.args[0])}]"
    if node.kind == "map":
        return f"map[{render_type(node.args[0])}, {render_type(node.args[1])}]"
    if node.kind == "tuple":
        return f"tuple[{', '.join(render_type(arg) for arg in node.args)}]"
    if node.kind == "union":
        return " | ".join(render_type(arg) for arg in node.args)
    raise CompileError(f"unsupported type node: {node.kind}")


def flatten_union(nodes: list[idl.TypeNode]) -> idl.TypeNode:
    flat: list[idl.TypeNode] = []
    seen: set[str] = set()

    def add(node: idl.TypeNode) -> None:
        if node.kind == "union":
            for child in node.args:
                add(child)
            return
        key = render_type(node)
        if key not in seen:
            seen.add(key)
            flat.append(node)

    for node in nodes:
        add(node)

    if not flat:
        raise CompileError("cannot create an empty type union")
    if len(flat) == 1:
        return flat[0]
    return idl.TypeNode(kind="union", args=flat)


class Compiler:
    def __init__(self, modules: list[idl.ModuleDef]):
        self.modules = modules
        self.symbol_index = idl.build_symbol_index(modules)
        self.enum_members = idl.build_enum_members(modules)
        idl.validate_schema(modules, self.symbol_index, self.enum_members)

        self.models: dict[str, idl.ModelDef] = {}
        self.model_order: list[str] = []
        self.children: dict[str, list[str]] = defaultdict(list)
        self.raw_models: dict[str, dict] = {}
        self.raw_vocabulary: dict[str, list[str]] = {}
        self.raw_maps: dict[str, dict] = {}

        for module in modules:
            raw = yaml.safe_load(module.path.read_text()) or {}
            for enum_name, entries in (raw.get("enums") or {}).items():
                self.raw_vocabulary[enum_name] = copy.deepcopy(entries)
            for map_name, spec in (raw.get("maps") or {}).items():
                self.raw_maps[map_name] = copy.deepcopy(spec)
            for model in module.models:
                if model.semantic_role not in {"concept", "type", "representation"}:
                    raise CompileError(
                        f"{module.path}: {model.name} must declare semantic_role concept, type, or representation"
                    )
                self.models[model.name] = model
                self.model_order.append(model.name)
            for model_name, spec in (raw.get("models") or {}).items():
                self.raw_models[model_name] = copy.deepcopy(spec)

        for model in self.models.values():
            if model.parent:
                self.children[model.parent].append(model.name)
        self.types: set[str] = {
            name for name, model in self.models.items() if model.semantic_role == "type"
        }
        self.representations: set[str] = {
            name for name, model in self.models.items() if model.semantic_role == "representation"
        }
        self.emitted_models = self.types | self.representations
        # Runtime model IDs are contract-local wire discriminators. They are
        # derived deterministically from the emitted model set; there is no
        # hand-maintained registry or compatibility reservation.
        self.model_ids = {
            name: model_id
            for model_id, name in enumerate(sorted(self.emitted_models), start=1)
        }

        self._descendant_cache: dict[str, list[str]] = {}
        self._effective_field_cache: dict[str, dict[str, object]] = {}

    def emitted_descendants(self, model_name: str) -> list[str]:
        cached = self._descendant_cache.get(model_name)
        if cached is not None:
            return cached

        result: list[str] = []
        seen: set[str] = set()

        def walk(name: str) -> None:
            for child in self.children.get(name, []):
                if child in seen:
                    continue
                seen.add(child)
                if child in self.emitted_models:
                    result.append(child)
                walk(child)

        walk(model_name)
        self._descendant_cache[model_name] = result
        return result

    def effective_fields(self, model_name: str) -> dict[str, object]:
        cached = self._effective_field_cache.get(model_name)
        if cached is not None:
            return copy.deepcopy(cached)

        lineage: list[str] = []
        seen: set[str] = set()
        current: str | None = model_name
        while current is not None:
            if current in seen:
                raise CompileError(f"model parent cycle involving {current}")
            seen.add(current)
            lineage.append(current)
            current = self.models[current].parent

        fields: dict[str, object] = {}
        for name in reversed(lineage):
            for field_name, field_spec in (self.raw_models[name].get("fields") or {}).items():
                # Replacing an inherited field keeps its original insertion
                # position, matching the effective runtime field ordering.
                fields[field_name] = copy.deepcopy(field_spec)

        self._effective_field_cache[model_name] = copy.deepcopy(fields)
        return fields

    def model_family(self, model_name: str) -> str:
        """Return the nearest ancestor Concept or Type of an emitted runtime model."""
        seen: set[str] = {model_name}
        current = self.models[model_name].parent
        while current is not None:
            if current in seen:
                raise CompileError(f"model parent cycle involving {current}")
            seen.add(current)

            parent = self.models.get(current)
            if parent is None:
                raise CompileError(f"model {model_name} has unknown parent {current}")
            if parent.semantic_role in {"concept", "type"}:
                return current
            current = parent.parent

        raise CompileError(
            f"emitted runtime model {model_name} has no ancestor Concept or Type to use as family"
        )

    def lower_named_type(self, name: str) -> idl.TypeNode:
        if name in idl.PRIMITIVE_TYPES or name in self.enum_members:
            return idl.TypeNode(kind="name", name=name)

        model = self.models.get(name)
        if model is None:
            return idl.TypeNode(kind="name", name=name)

        # Type and Representation references are exact. Concept references are
        # semantic shorthand that must be resolved to the emitted runtime forms
        # currently available beneath them.
        if name in self.emitted_models:
            return idl.TypeNode(kind="name", name=name)

        candidates = self.emitted_descendants(name)
        if not candidates:
            raise CompileError(f"Concept {name} has no emitted Type or Representation descendants")
        return flatten_union([idl.TypeNode(kind="name", name=item) for item in candidates])

    def lower_type(self, node: idl.TypeNode) -> idl.TypeNode:
        if node.kind == "fixed_bytes":
            return copy.deepcopy(node)
        if node.kind == "name":
            assert node.name is not None
            return self.lower_named_type(node.name)
        if node.kind == "semantic":
            # Semantic arguments name the namespace exactly as authored; they are
            # not runtime type references and must not be lowered through the
            # Concept hierarchy.
            return copy.deepcopy(node)
        if node.kind in {"list", "map", "tuple"}:
            return idl.TypeNode(kind=node.kind, args=[self.lower_type(arg) for arg in node.args])
        if node.kind == "union":
            return flatten_union([self.lower_type(arg) for arg in node.args])
        raise CompileError(f"unsupported type node: {node.kind}")

    def rewrite_field(self, field_name: str, spec: object) -> object:
        if isinstance(spec, dict):
            result = copy.deepcopy(spec)
            if "type" not in result:
                raise CompileError(f"expanded field {field_name} is missing type")
            type_text = str(result["type"]).strip()
            optional, type_text = idl.strip_prefix(type_text, "optional ")
            const, type_text = idl.strip_prefix(type_text, "const ")
            lowered = render_type(self.lower_type(idl.TypeParser(type_text).parse()))
            prefix = "optional " if optional else ("const " if const else "")
            result["type"] = prefix + lowered
            return result

        if not isinstance(spec, str):
            raise CompileError(f"unsupported field syntax for {field_name}: {spec!r}")

        type_text, default_text = idl.split_default(spec)
        optional, type_text = idl.strip_prefix(type_text, "optional ")
        const, type_text = idl.strip_prefix(type_text, "const ")
        lowered = render_type(self.lower_type(idl.TypeParser(type_text).parse()))
        prefix = "optional " if optional else ("const " if const else "")
        value = prefix + lowered
        if default_text is not None:
            value += f" = {default_text}"
        return value

    def compile_model(self, model_name: str) -> dict[str, object]:
        model = self.models[model_name]
        out: dict[str, object] = {
            "model_id": self.model_ids[model_name],
            "package": self.symbol_index[model_name],
            "family": self.model_family(model_name),
        }
        if model.description:
            out["description"] = model.description
        if model.value_type is not None:
            inherited_fields = self.effective_fields(model_name)
            if inherited_fields:
                raise CompileError(
                    f"atomic representation {model_name} cannot inherit or declare fields: "
                    f"{', '.join(inherited_fields)}"
                )
            out["type"] = render_type(self.lower_type(model.value_type))
            return out
        fields = {
            field_name: self.rewrite_field(field_name, field_spec)
            for field_name, field_spec in self.effective_fields(model_name).items()
        }
        if fields:
            out["fields"] = fields
        return out

    def compile(self) -> dict[str, object]:
        vocabulary: dict[str, dict[str, object]] = {}
        maps: dict[str, dict[str, object]] = {}
        types: dict[str, dict[str, object]] = {}
        representations: dict[str, dict[str, object]] = {}

        for module in self.modules:
            for enum in module.enums:
                vocabulary[enum.name] = {
                    "package": module.name,
                    "values": copy.deepcopy(self.raw_vocabulary[enum.name]),
                }
            for mapping in module.maps:
                maps[mapping.name] = {
                    "package": module.name,
                    **copy.deepcopy(self.raw_maps[mapping.name]),
                }

        for model_name in self.model_order:
            if model_name in self.types:
                types[model_name] = self.compile_model(model_name)
            elif model_name in self.representations:
                representations[model_name] = self.compile_model(model_name)

        return {
            "version": 1,
            "type": "occid",
            "vocabulary": vocabulary,
            "types": types,
            "representations": representations,
            "maps": maps,
        }


def _dump_entry(name: str, value: object) -> list[str]:
    text = yaml.safe_dump(
        {name: value},
        sort_keys=False,
        allow_unicode=True,
        width=1e10,
    ).rstrip()
    return [f"  {line}" for line in text.splitlines()]


def render_compiled_yaml(compiled: dict[str, object]) -> str:
    lines = [
        "# GENERATED by compile_occid.py. Do not edit.",
        "# Concept hierarchy is compile-time input; runtime contains Types, Representations, and Vocabulary.",
        f"version: {compiled['version']}",
        f"type: {compiled['type']}",
        "",
    ]

    for section_name in ("vocabulary", "types", "representations", "maps"):
        section = compiled[section_name]
        assert isinstance(section, dict)
        lines.append(f"{section_name}:")
        if not section:
            lines[-1] += " {}"
            lines.append("")
            continue
        entries = list(section.items())
        for index, (name, value) in enumerate(entries):
            lines.extend(_dump_entry(name, value))
            if index != len(entries) - 1:
                lines.append("")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    modules = idl.load_modules(args.schema_dir, args.module_dir, [], [], True)
    compiler = Compiler(modules)
    compiled = compiler.compile()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_compiled_yaml(compiled))

    concept_count = sum(model.semantic_role == "concept" for model in compiler.models.values())
    print(f"output={args.output}")
    print(f"concepts_consumed={concept_count - len(compiler.types)}")
    print(f"types={len(compiler.types)}")
    print(f"representations={len(compiler.representations)}")
    print(f"vocabulary={len(compiled['vocabulary'])}")
    print(f"maps={len(compiled['maps'])}")


if __name__ == "__main__":
    main()
