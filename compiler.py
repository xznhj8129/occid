from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml


def parse_enum_items(items: list[str]) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    next_value = 0
    for raw in items:
        text = str(raw).strip()
        if "=" in text:
            name, value = (part.strip() for part in text.split("=", 1))
            next_value = int(value)
        else:
            name = text
        out.append((name, next_value))
        next_value += 1
    return out


def topo_models(models: dict[str, dict[str, Any]]) -> list[str]:
    result: list[str] = []
    pending = list(models)
    while pending:
        progressed = False
        for name in list(pending):
            parent = models[name].get("parent")
            if parent is None or parent in result:
                result.append(name)
                pending.remove(name)
                progressed = True
        if not progressed:
            raise ValueError(f"parent cycle or missing parent among: {pending}")
    return result


def parse_field(raw: str) -> tuple[str, str | None]:
    text = raw.strip()
    if "=" in text:
        type_part, default = (x.strip() for x in text.split("=", 1))
        return type_part, default
    return text, None


def py_type(type_expr: str, known_enums: set[str], known_models: set[str]) -> tuple[str, str | None]:
    type_expr = type_expr.strip()
    if type_expr.startswith("optional "):
        inner, _ = py_type(type_expr[len("optional "):], known_enums, known_models)
        return f"{inner} | None", "None"
    if type_expr.startswith("list[") and type_expr.endswith("]"):
        inner_text = type_expr[5:-1]
        inner, _ = py_type(inner_text, known_enums, known_models)
        return f"list[{inner}]", "factory:list"
    primitive = {
        "string": "str",
        "float": "float",
        "int": "int",
        "bool": "bool",
        "UID": "str",
    }
    if type_expr in primitive:
        return primitive[type_expr], None
    if type_expr in known_enums or type_expr in known_models:
        return type_expr, None
    return "Any", None


def model_semantics(models: dict[str, dict[str, Any]], order: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for name in order:
        spec = models[name]
        inherited = list(out.get(spec.get("parent"), []))
        terms = inherited
        if spec.get("semantic_role") == "concept":
            terms = terms + [name]
        terms = terms + list(spec.get("product", []))
        # Preserve deterministic order while eliminating duplicates.
        out[name] = list(OrderedDict((x, None) for x in terms).keys())
    return out


def expand_terms(terms: list[str], semantics: dict[str, list[str]]) -> list[str]:
    expanded: list[str] = []
    for term in terms:
        if term in semantics:
            expanded.extend(semantics[term])
        else:
            expanded.append(term)
    return list(OrderedDict((x, None) for x in expanded).keys())


def compile_schema(schema_path: Path, output_dir: Path) -> None:
    schema = yaml.safe_load(schema_path.read_text())
    output_dir.mkdir(parents=True, exist_ok=True)

    axes: dict[str, dict[str, Any]] = schema.get("axes", {})
    enums: dict[str, list[str]] = schema.get("enums", {})
    models: dict[str, dict[str, Any]] = schema.get("models", {})
    codewords: dict[str, dict[str, Any]] = schema.get("codewords", {})
    relations: dict[str, dict[str, Any]] = schema.get("relations", {})

    order = topo_models(models)
    semantics = model_semantics(models, order)
    known_enums = set(enums)
    known_models = set(models)

    expanded_codewords = {
        key: expand_terms(list(value.get('product', [])), semantics)
        for key, value in codewords.items()
    }

    registry = {
        "axes": axes,
        "models": {
            name: {
                "semantic_role": models[name].get("semantic_role"),
                "parent": models[name].get("parent"),
                "semantics": semantics[name],
                "fields": list((models[name].get("fields") or {}).keys()),
            }
            for name in order
        },
        "codewords": expanded_codewords,
        "relations": {
            name: list(spec.get("signature", [])) for name, spec in relations.items()
        },
    }

    (output_dir / "semantic_registry.json").write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n"
    )

    lines: list[str] = [
        "# GENERATED FILE - DO NOT EDIT",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass, field",
        "from typing import Any, ClassVar",
        "",
        "from runtime import (",
        "    AxisValue,",
        "    RelationType,",
        "    SemanticAxis,",
        "    SemanticEnum,",
        "    SemanticModel,",
        "    SemanticRegistry,",
        "    Store,",
        "    product_names,",
        ")",
        "",
    ]

    for axis_name, axis in axes.items():
        lines += [
            f"class {axis_name}(SemanticAxis):",
            f"    _axis_name = {axis_name!r}",
            f"    _cardinality = {axis.get('cardinality', 'many')!r}",
            f"    _applies = {axis.get('applies')!r}",
            "",
        ]
        for value in axis.get("values", []):
            lines.append(f"{axis_name}.{value} = AxisValue({axis_name!r}, {value!r})")
        lines.append("")

    enum_values: dict[str, list[tuple[str, int]]] = {}
    for enum_name, items in enums.items():
        parsed = parse_enum_items(items)
        enum_values[enum_name] = parsed
        lines += [f"class {enum_name}(SemanticEnum):"]
        for item_name, item_value in parsed:
            lines.append(f"    {item_name} = {item_value}")
        if not parsed:
            lines.append("    pass")
        lines.append("")
        mapping_lines = []
        for item_name, _ in parsed:
            key = f"{enum_name}.{item_name}"
            if key in codewords:
                mapping_lines.append(
                    f"    {item_name!r}: product_names({expanded_codewords[key]!r}),"
                )
        lines += [f"{enum_name}._semantic_map = {{", *mapping_lines, "}", ""]

    for name in order:
        spec = models[name]
        parent = spec.get("parent") or "SemanticModel"
        lines += ["@dataclass(kw_only=True)", f"class {name}({parent}):"]
        lines.append(f"    _semantic_role: ClassVar[str] = {spec.get('semantic_role', 'concept')!r}")
        lines.append(f"    _semantics: ClassVar = product_names({semantics[name]!r})")
        declared = list((spec.get("fields") or {}).keys())
        lines.append(f"    _declared_fields: ClassVar[tuple[str, ...]] = {tuple(declared)!r}")
        field_specs = spec.get("fields") or {}
        for field_name, raw in field_specs.items():
            type_expr, explicit_default = parse_field(str(raw))
            annotation, inferred_default = py_type(type_expr, known_enums, known_models)
            default = explicit_default if explicit_default is not None else inferred_default
            if default == "factory:list":
                lines.append(f"    {field_name}: {annotation} = field(default_factory=list)")
            elif default is None:
                lines.append(f"    {field_name}: {annotation}")
            elif default == "None":
                lines.append(f"    {field_name}: {annotation} = None")
            elif type_expr in known_enums:
                lines.append(f"    {field_name}: {annotation} = {type_expr}.{default}")
            else:
                if default.lower() in {"true", "false"}:
                    default_py = default.title()
                else:
                    try:
                        float(default)
                        default_py = default
                    except ValueError:
                        default_py = repr(default)
                lines.append(f"    {field_name}: {annotation} = {default_py}")
        lines.append("")

    for relation_name, spec in relations.items():
        signature = ", ".join(spec.get("signature", []))
        if len(spec.get("signature", [])) == 1:
            signature += ","
        lines.append(
            f"{relation_name} = RelationType({relation_name!r}, ({signature}))"
        )
    lines.append("")

    lines += [
        f"REGISTRY_SPEC = {registry!r}",
        "REGISTRY = SemanticRegistry(REGISTRY_SPEC)",
        "",
        "def new_store() -> Store:",
        "    return Store(REGISTRY)",
        "",
    ]

    (output_dir / "occid2.py").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path, nargs="?", default=Path("occid2.schema.yaml"))
    parser.add_argument("--out", type=Path, default=Path("generated"))
    args = parser.parse_args()
    compile_schema(args.schema, args.out)


if __name__ == "__main__":
    main()
