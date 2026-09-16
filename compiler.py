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


def normalize_field(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        if "type" not in raw:
            raise ValueError(f"field declaration is missing 'type': {raw!r}")
        type_expr = str(raw["type"])
        explicit_default = raw.get("default")
        return {
            "type": type_expr,
            "default": None if explicit_default is None else str(explicit_default),
        }
    text = str(raw).strip()
    if "=" in text:
        type_part, default = (x.strip() for x in text.split("=", 1))
        return {"type": type_part, "default": default}
    return {"type": text, "default": None}


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
    raise ValueError(f"unknown type name: {type_expr!r}")


def render_default(
    type_expr: str,
    default: str,
    known_enums: set[str],
    enum_values: dict[str, list[tuple[str, int]]],
) -> str:
    base = type_expr.strip()
    if base.startswith("optional "):
        base = base[len("optional "):].strip()
    if base in known_enums:
        members = {item_name for item_name, _ in enum_values.get(base, [])}
        if default not in members:
            raise ValueError(f"{default!r} is not a member of {base}")
        return f"{base}.{default}"
    if base in ("string", "UID"):
        return repr(default)
    if base == "float":
        try:
            float(default)
        except ValueError as exc:
            raise ValueError(f"{default!r} is not a float") from exc
        return default
    if base == "int":
        try:
            int(default)
        except ValueError as exc:
            raise ValueError(f"{default!r} is not an int") from exc
        return default
    if base == "bool":
        if default.lower() not in {"true", "false"}:
            raise ValueError(f"{default!r} is not a bool")
        return default.title()
    raise ValueError(f"cannot render default for type {type_expr!r}")


def model_semantics(models: dict[str, dict[str, Any]], order: list[str]) -> dict[str, list[str]]:
    # Every model is a named product: its name is a factor, parentage entails
    # the parent's full resolved semantics, and a product entry naming another
    # model expands to that model's full semantics.
    resolved: dict[str, list[str]] = {}
    resolving: list[str] = []

    def resolve(name: str) -> list[str]:
        if name in resolved:
            return resolved[name]
        if name in resolving:
            raise ValueError(f"product cycle: {' -> '.join(resolving + [name])}")
        resolving.append(name)
        parent = models[name].get("parent")
        terms = list(resolve(parent)) if parent else []
        terms.append(name)
        for term in models[name].get("product", []):
            if term in models:
                terms.extend(resolve(term))
            else:
                terms.append(term)
        resolving.pop()
        resolved[name] = list(OrderedDict((x, None) for x in terms).keys())
        return resolved[name]

    for name in order:
        resolve(name)
    return resolved


def expand_terms(terms: list[str], semantics: dict[str, list[str]]) -> list[str]:
    expanded: list[str] = []
    for term in terms:
        if term in semantics:
            expanded.extend(semantics[term])
        else:
            expanded.append(term)
    return list(OrderedDict((x, None) for x in expanded).keys())


def resolve_aliases(
    raw_aliases: dict[str, list[str]], semantics: dict[str, list[str]]
) -> dict[str, list[str]]:
    # Aliases are products and may name other aliases; resolve canonically,
    # expanding every referenced alias and model to its terms.
    resolved: dict[str, list[str]] = {}
    resolving: list[str] = []

    def resolve(name: str) -> list[str]:
        if name in resolved:
            return resolved[name]
        if name in resolving:
            raise ValueError(f"alias cycle: {' -> '.join(resolving + [name])}")
        resolving.append(name)
        terms: list[str] = []
        for term in raw_aliases[name]:
            if term in raw_aliases:
                terms.extend(resolve(term))
            elif term in semantics:
                terms.extend(semantics[term])
            else:
                terms.append(term)
        resolving.pop()
        resolved[name] = list(OrderedDict((x, None) for x in terms).keys())
        return resolved[name]

    for alias_name in raw_aliases:
        resolve(alias_name)
    return resolved


def normalize_axis(axis: dict[str, Any]) -> dict[str, Any]:
    # Axis values may be a list of names or a mapping name -> declaration, where
    # a declaration carries applies/requires/disjoint/excludes for that value.
    names: list[str] = []
    value_meta: dict[str, dict[str, Any]] = {}
    raw_values = axis.get("values", [])
    if isinstance(raw_values, dict):
        entries = list(raw_values.items())
    else:
        entries = []
        for raw in raw_values:
            if isinstance(raw, dict):
                entries.extend(raw.items())
            else:
                entries.append((raw, None))
    for name, declaration in entries:
        names.append(str(name))
        if declaration:
            value_meta[str(name)] = dict(declaration)
    normalized = dict(axis)
    normalized["values"] = names
    if value_meta:
        normalized["value_meta"] = value_meta
    return normalized


def normalize_relation(spec: dict[str, Any]) -> dict[str, Any]:
    # Positional `signature: [A, B]` or named `operands: {source: A, target: B}`.
    # Named operands keep order; `specializes` inherits direction from a base.
    operands = spec.get("operands")
    if operands:
        pairs = [(str(name), str(region)) for name, region in operands.items()]
        signature = [region for _, region in pairs]
        operand_names = [name for name, _ in pairs]
    else:
        signature = [str(x) for x in spec.get("signature", [])]
        operand_names = []
    return {
        "signature": signature,
        "operand_names": operand_names,
        "specializes": spec.get("specializes"),
    }


def order_relations(relations: dict[str, dict[str, Any]]) -> list[str]:
    result: list[str] = []
    pending = list(relations)
    while pending:
        progressed = False
        for name in list(pending):
            base = relations[name].get("specializes")
            if not base or base in result:
                result.append(name)
                pending.remove(name)
                progressed = True
        if not progressed:
            raise ValueError(f"relation specialization cycle or missing base among: {pending}")
    return result


CONSTRAINT_KEYS = ("applies", "requires", "disjoint", "excludes")


def compile_schema(schema_path: Path, output_dir: Path) -> None:
    schema = yaml.safe_load(schema_path.read_text())
    output_dir.mkdir(parents=True, exist_ok=True)

    axes: dict[str, dict[str, Any]] = {
        name: normalize_axis(axis) for name, axis in (schema.get("axes") or {}).items()
    }
    enums: dict[str, list[str]] = schema.get("enums", {})
    models: dict[str, dict[str, Any]] = schema.get("models", {})
    codewords: dict[str, dict[str, Any]] = schema.get("codewords", {})
    relation_specs: dict[str, dict[str, Any]] = {
        name: normalize_relation(spec)
        for name, spec in (schema.get("relations") or {}).items()
    }

    order = topo_models(models)
    semantics = model_semantics(models, order)
    known_enums = set(enums)
    known_models = set(models)

    for relation_name, relation in relation_specs.items():
        for region in relation["signature"]:
            if region not in models:
                raise ValueError(f"relation {relation_name}: unknown operand region {region!r}")
        base = relation["specializes"]
        if base and base not in relation_specs:
            raise ValueError(f"relation {relation_name}: unknown base relation {base!r}")
    order_relations(relation_specs)

    expanded_codewords = {
        key: expand_terms(list(value.get('product', [])), semantics)
        for key, value in codewords.items()
    }
    codeword_relations = {
        key: str(value["relation"])
        for key, value in codewords.items()
        if value.get("relation")
    }

    raw_aliases: dict[str, list[str]] = dict(schema.get("aliases") or {})
    for alias_name in raw_aliases:
        if alias_name in models or alias_name in enums:
            raise ValueError(f"alias collides with a class or enum: {alias_name}")
    aliases = resolve_aliases(raw_aliases, semantics)

    registry = {
        "axes": axes,
        "models": {
            name: {
                "parent": models[name].get("parent"),
                "semantics": semantics[name],
                "fields": [
                    {"name": field_name, **normalize_field(raw)}
                    for field_name, raw in (models[name].get("fields") or {}).items()
                ],
                **{
                    key: models[name][key]
                    for key in CONSTRAINT_KEYS
                    if models[name].get(key)
                },
            }
            for name in order
        },
        "codewords": expanded_codewords,
        "codeword_relations": codeword_relations,
        "aliases": aliases,
        "relations": relation_specs,
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

    # Named aliases are products, not classes.
    for alias_name, terms in aliases.items():
        lines += [f"{alias_name} = product_names({terms!r})", ""]

    for name in order:
        spec = models[name]
        parent = spec.get("parent") or "SemanticModel"
        lines += ["@dataclass(kw_only=True)", f"class {name}({parent}):"]
        lines.append(f"    _semantics: ClassVar = product_names({semantics[name]!r})")
        declared = list((spec.get("fields") or {}).keys())
        lines.append(f"    _declared_fields: ClassVar[tuple[str, ...]] = {tuple(declared)!r}")
        field_specs = spec.get("fields") or {}
        for field_name, raw in field_specs.items():
            try:
                field_spec = normalize_field(raw)
                type_expr = field_spec["type"]
                explicit_default = field_spec["default"]
                annotation, inferred_default = py_type(type_expr, known_enums, known_models)
                default = explicit_default if explicit_default is not None else inferred_default
                if default == "factory:list":
                    lines.append(f"    {field_name}: {annotation} = field(default_factory=list)")
                elif default is None:
                    lines.append(f"    {field_name}: {annotation}")
                elif default == "None":
                    lines.append(f"    {field_name}: {annotation} = None")
                elif explicit_default is not None:
                    default_py = render_default(type_expr, default, known_enums, enum_values)
                    lines.append(f"    {field_name}: {annotation} = {default_py}")
                else:
                    lines.append(f"    {field_name}: {annotation}")
            except ValueError as exc:
                raise ValueError(f"{name}.{field_name}: {exc}") from exc
        lines.append("")

    for relation_name in order_relations(relation_specs):
        spec = relation_specs[relation_name]
        signature = ", ".join(spec["signature"])
        if len(spec["signature"]) == 1:
            signature += ","
        kwargs = ""
        if spec["operand_names"]:
            kwargs += f", operand_names={tuple(spec['operand_names'])!r}"
        if spec["specializes"]:
            kwargs += f", base={spec['specializes']}"
        lines.append(
            f"{relation_name} = RelationType({relation_name!r}, ({signature}){kwargs})"
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
