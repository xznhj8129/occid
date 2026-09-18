from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml

PRODUCT_SPLIT = re.compile(r"\s*[*\u00d7]\s*")
UNIT_RE = re.compile(r"^(?P<kind>[A-Za-z_]\w*)\s*\[(?P<unit>[^\]]+)\]\s*$")
EQUATION_RE = re.compile(
    r"^\s*(?P<quantity>[A-Za-z_]\w*)\s*\(\s*(?P<of>[A-Za-z_]\w*)\s*\)"
    r"\s*=\s*(?P<equals>[A-Za-z_]\w*)\s*$"
)
CONSTRAINT_KEYS = ("applies", "requires", "disjoint", "excludes")


def unique(items: list[str]) -> list[str]:
    return list(OrderedDict((item, None) for item in items).keys())


def split_product(text: Any) -> list[str]:
    return [part.strip() for part in PRODUCT_SPLIT.split(str(text)) if part.strip()]


def term_list(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    return [str(item) for item in raw]


def product_terms(raw: Any) -> list[str]:
    terms: list[str] = []
    for item in term_list(raw):
        terms.extend(split_product(item))
    return terms


def parse_coordinate(name: str, raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        raw = raw.get("type", "")
    text = str(raw).strip()
    match = UNIT_RE.match(text)
    if match:
        return {"name": name, "type": match.group("kind"), "unit": match.group("unit")}
    return {"name": name, "type": text, "unit": None}


def parse_equation(text: Any) -> dict[str, str] | None:
    match = EQUATION_RE.match(str(text).strip())
    return dict(match.groupdict()) if match else None


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


def py_type(
    type_expr: str,
    known_enums: set[str],
    known_models: set[str],
    declared: bool = True,
) -> tuple[str, str | None]:
    type_expr = type_expr.strip()
    if type_expr.startswith("optional "):
        inner, _ = py_type(type_expr[len("optional "):], known_enums, known_models, declared)
        return f"{inner} | None", "None"
    if type_expr.startswith("list[") and type_expr.endswith("]"):
        inner_text = type_expr[5:-1]
        inner, _ = py_type(inner_text, known_enums, known_models, declared)
        return f"list[{inner}]", "factory:list"
    primitive = {
        "string": "str",
        "float": "float",
        "int": "int",
        "bool": "bool",
        "UID": "str",
    }
    if declared:
        # Declared fields are subject matter, not data: a plain scalar must be
        # reduced through a chart representation. A named model shadows any
        # same-named primitive. Only `bool` survives as an irreducible leaf.
        if type_expr in known_enums or type_expr in known_models:
            return type_expr, None
        if type_expr == "bool":
            return "bool", None
        raise ValueError(
            f"declared field type {type_expr!r} must be a model or enum; "
            f"plain primitives are chart variables"
        )
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
    # Every model is a named product: its own name, the factors it inherits,
    # and its own `product:`/`chart:` factors. Parentage entails the parent's
    # meaning, but an ancestor's name is a label, not a factor: inheritance
    # carries the parent's factors and drops its labels, which the solver
    # re-derives from parentage. Naming a model in `product:` keeps that
    # model's label, because it is part of this model's own meaning. A
    # `chart:` key contributes its factors and compiles its variables.
    resolved: dict[str, list[str]] = {}
    resolving: list[str] = []

    def resolve(name: str) -> list[str]:
        if name in resolved:
            return resolved[name]
        if name in resolving:
            raise ValueError(f"product cycle: {' -> '.join(resolving + [name])}")
        resolving.append(name)
        spec = models[name]
        parent = spec.get("parent")
        terms = [term for term in resolve(parent) if term not in models] if parent else []
        terms.append(name)
        raw_products = term_list(spec.get("product"))
        if spec.get("chart"):
            raw_products.append(spec["chart"])
        for raw in raw_products:
            for term in split_product(raw):
                if term in models:
                    terms.extend(resolve(term))
                else:
                    terms.append(term)
        resolving.pop()
        resolved[name] = unique(terms)
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
    return unique(expanded)


def semantic_closure(
    terms: list[str],
    semantics: dict[str, list[str]],
    models: dict[str, dict[str, Any]],
) -> set[str]:
    # Entailment closure of model names: a model entails its own factors and,
    # through parentage, every ancestor name.
    out: set[str] = set()
    stack = list(terms)
    while stack:
        term = stack.pop()
        if term in out:
            continue
        out.add(term)
        stack.extend(semantics.get(term, ()))
        parent = models.get(term, {}).get("parent")
        if parent:
            stack.append(parent)
    return out


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
        for raw in term_list(raw_aliases[name]):
            for term in split_product(raw):
                if term in raw_aliases:
                    terms.extend(resolve(term))
                elif term in semantics:
                    terms.extend(semantics[term])
                else:
                    terms.append(term)
        resolving.pop()
        resolved[name] = unique(terms)
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
    # Named `operands: {role: region}` or positional `signature: [A, B]`.
    # Roles and order belong to the relation itself.
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
    }


def compile_charts(
    raw_charts: dict[str, Any], semantics: dict[str, list[str]]
) -> list[dict[str, Any]]:
    charts: list[dict[str, Any]] = []
    for key_text, raw_coords in (raw_charts or {}).items():
        terms: list[str] = []
        for term in split_product(key_text):
            if term in semantics:
                terms.extend(semantics[term])
            else:
                terms.append(term)
        coords = [
            parse_coordinate(str(name), raw)
            for name, raw in (raw_coords or {}).items()
        ]
        charts.append(
            {"display": str(key_text), "factors": unique(terms), "coords": coords}
        )
    return charts


def charts_entailed(
    terms: list[str],
    charts: list[dict[str, Any]],
    semantics: dict[str, list[str]],
    models: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    closed = semantic_closure(terms, semantics, models)
    return [
        chart
        for chart in charts
        if semantic_closure(chart["factors"], semantics, models) <= closed
    ]


def compile_schema(schema_path: Path, output_dir: Path) -> None:
    schema = yaml.safe_load(schema_path.read_text())
    output_dir.mkdir(parents=True, exist_ok=True)

    axes: dict[str, dict[str, Any]] = {
        name: normalize_axis(axis) for name, axis in (schema.get("axes") or {}).items()
    }
    enums: dict[str, list[str]] = schema.get("enums", {})
    models: dict[str, dict[str, Any]] = schema.get("models", {})
    projections_raw: dict[str, dict[str, Any]] = schema.get("projections", {})
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

    charts = compile_charts(schema.get("charts") or {}, semantics)

    raw_aliases: dict[str, list[str]] = dict(schema.get("aliases") or {})
    for alias_name in raw_aliases:
        if alias_name in models or alias_name in enums:
            raise ValueError(f"alias collides with a class or enum: {alias_name}")
    aliases = resolve_aliases(raw_aliases, semantics)

    expressions: dict[str, dict[str, Any]] = {}
    word_expressions: dict[str, str] = {}
    for expression_name, spec in (schema.get("expressions") or {}).items():
        # Variable regions stay as authored; binding validation compares a
        # region against the semantic closure of the bound value.
        given = {
            str(role): product_terms(region)
            for role, region in (spec.get("given") or {}).items()
        }
        sought = {
            str(role): product_terms(region)
            for role, region in (spec.get("sought") or {}).items()
        }
        equations: list[dict[str, str]] = []
        for raw in spec.get("equations") or []:
            parsed = parse_equation(raw)
            if parsed is not None:
                equations.append(parsed)
        words = [str(word) for word in (spec.get("words") or [])]
        for word in words:
            if word in word_expressions:
                raise ValueError(f"word {word!r} names more than one expression")
            word_expressions[word] = expression_name
        expressions[expression_name] = {
            "description": spec.get("description"),
            "factors": expand_terms(product_terms(spec.get("factors")), semantics),
            "given": given,
            "sought": sought,
            "equations": equations,
            "words": words,
        }

    # A word must name a declared enum member or axis value; the compiler
    # never silently drops a misspelled word.
    enum_members = {
        name: {member for member, _ in parse_enum_items(items)}
        for name, items in enums.items()
    }
    for word in word_expressions:
        owner, _, member = word.partition(".")
        if owner in enum_members:
            if member not in enum_members[owner]:
                raise ValueError(f"word {word!r} is not a member of enum {owner}")
        elif owner in axes:
            if member not in axes[owner]["values"]:
                raise ValueError(f"word {word!r} is not a value of axis {owner}")
        else:
            raise ValueError(f"word {word!r} names neither an enum nor an axis")

    # Generated names share one module namespace; two declarations with the
    # same name would silently overwrite each other.
    declared: dict[str, str] = {}

    def declare(kind: str, names: Any) -> None:
        for name in names:
            other = declared.setdefault(str(name), kind)
            if other != kind:
                raise ValueError(f"{name!r} is declared as both {other} and {kind}")

    declare("axis", axes)
    declare("enum", enums)
    declare("model", models)
    declare("alias", raw_aliases)
    declare("expression", expressions)
    declare("projection", projections_raw)
    declare("relation", relation_specs)

    # -- models ------------------------------------------------------------

    model_entries: dict[str, dict[str, Any]] = {}
    for name in order:
        spec = models[name]
        selected = charts_entailed(semantics[name], charts, semantics, models)
        fields: list[dict[str, Any]] = []
        seen: set[str] = set()
        for field_name, raw in (spec.get("fields") or {}).items():
            fields.append({"name": field_name, **normalize_field(raw)})
            seen.add(field_name)
        for chart in selected:
            for coord in chart["coords"]:
                if coord["name"] in seen:
                    raise ValueError(f"{name}: chart field {coord['name']!r} collides")
                seen.add(coord["name"])
                fields.append(
                    {
                        "name": coord["name"],
                        "type": coord["type"],
                        "default": None,
                        "unit": coord["unit"],
                        "chart": chart["display"],
                    }
                )
        model_entries[name] = {
            "parent": spec.get("parent"),
            "semantics": semantics[name],
            "fields": fields,
            "chart_fields": [
                {"chart": chart["display"], "coords": chart["coords"]}
                for chart in selected
            ],
            **{key: spec[key] for key in CONSTRAINT_KEYS if spec.get(key)},
        }

    # -- projections -------------------------------------------------------

    projection_entries: dict[str, dict[str, Any]] = {}
    for name, spec in projections_raw.items():
        terms: list[str] = []
        selected: list[dict[str, Any]] = []
        seen_charts: set[str] = set()
        for raw in term_list(spec.get("product")):
            entry_terms: list[str] = []
            for term in split_product(raw):
                if term in semantics:
                    entry_terms.extend(semantics[term])
                else:
                    entry_terms.append(term)
            terms.extend(entry_terms)
            # Each listed product is one fact; only the charts it entails are
            # reduced into the projection's normal form.
            for chart in charts_entailed(entry_terms, charts, semantics, models):
                if chart["display"] not in seen_charts:
                    seen_charts.add(chart["display"])
                    selected.append(chart)
        terms = unique(terms)
        fields: list[dict[str, Any]] = []
        seen: set[str] = set()
        for field_name, raw in (spec.get("fields") or {}).items():
            fields.append({"name": field_name, **normalize_field(raw)})
            seen.add(field_name)
        for chart in selected:
            for coord in chart["coords"]:
                if coord["name"] in seen:
                    raise ValueError(f"{name}: chart field {coord['name']!r} collides")
                seen.add(coord["name"])
                fields.append(
                    {
                        "name": coord["name"],
                        "type": coord["type"],
                        "default": None,
                        "unit": coord["unit"],
                        "chart": chart["display"],
                        "optional": True,
                    }
                )
        projection_entries[name] = {
            "semantics": terms,
            "fields": fields,
            "charts": [chart["display"] for chart in selected],
        }

    # -- registry ----------------------------------------------------------

    registry = {
        "axes": axes,
        "models": model_entries,
        "charts": charts,
        "expressions": expressions,
        "word_expressions": word_expressions,
        "aliases": aliases,
        "relations": relation_specs,
        "projections": projection_entries,
    }

    (output_dir / "semantic_registry.json").write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n"
    )

    # -- generated python --------------------------------------------------

    lines: list[str] = [
        "# GENERATED FILE - DO NOT EDIT",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass, field",
        "from typing import Any, ClassVar",
        "",
        "from runtime import (",
        "    AxisValue,",
        "    Equation,",
        "    ExpressionType,",
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

    def product_literal(terms: list[str]) -> str:
        return f"product_names({list(terms)!r})"

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
            expression_name = word_expressions.get(key)
            if expression_name is not None:
                mapping_lines.append(
                    f"    {item_name!r}: {product_literal(expressions[expression_name]['factors'])},"
                )
        lines += [f"{enum_name}._semantic_map = {{", *mapping_lines, "}", ""]

    for expression_name, expression in expressions.items():
        lines.append(f"{expression_name} = ExpressionType(")
        lines.append(f"    {expression_name!r},")
        lines.append(f"    {product_literal(expression['factors'])}, ")
        lines.append(
            "    given={"
            + ", ".join(
                f"{role!r}: {product_literal(region)}"
                for role, region in expression["given"].items()
            )
            + "},"
        )
        lines.append(
            "    sought={"
            + ", ".join(
                f"{role!r}: {product_literal(region)}"
                for role, region in expression["sought"].items()
            )
            + "},"
        )
        equation_items = ", ".join(
            f"Equation({eq['quantity']!r}, {eq['of']!r}, {eq['equals']!r})"
            for eq in expression["equations"]
        )
        if equation_items:
            equation_items += ","
        lines.append(f"    equations=({equation_items}),")
        lines.append(f"    words={tuple(expression['words'])!r},")
        lines.append(")")
        lines.append("")

    # Named aliases are products, not classes.
    for alias_name, terms in aliases.items():
        lines += [f"{alias_name} = {product_literal(terms)}", ""]

    def emit_dataclass(
        name: str,
        parent: str,
        semantics_terms: list[str],
        fields: list[dict[str, Any]],
        charts: list[str],
        projection: bool,
    ) -> None:
        lines.append("@dataclass(kw_only=True)")
        lines.append(f"class {name}({parent}):")
        lines.append(f"    _semantics: ClassVar = {product_literal(semantics_terms)}")
        lines.append(
            f"    _declared_fields: ClassVar[tuple[str, ...]] = {tuple(f['name'] for f in fields)!r}"
        )
        units = {f["name"]: f["unit"] for f in fields if f.get("unit")}
        lines.append(f"    _units: ClassVar[dict[str, str]] = {units!r}")
        lines.append(f"    _charts: ClassVar[tuple[str, ...]] = {tuple(charts)!r}")
        if projection:
            lines.append("    _projection: ClassVar[bool] = True")
        for field_spec in fields:
            field_name = field_spec["name"]
            annotation, inferred_default = py_type(
                field_spec["type"], known_enums, known_models,
                declared=not field_spec.get("chart"),
            )
            explicit_default = field_spec.get("default")
            if field_spec.get("optional"):
                lines.append(f"    {field_name}: {annotation} | None = None")
            elif explicit_default is not None:
                default_py = render_default(
                    field_spec["type"], explicit_default, known_enums, enum_values
                )
                lines.append(f"    {field_name}: {annotation} = {default_py}")
            elif inferred_default == "factory:list":
                lines.append(f"    {field_name}: {annotation} = field(default_factory=list)")
            elif inferred_default == "None":
                lines.append(f"    {field_name}: {annotation} = None")
            else:
                lines.append(f"    {field_name}: {annotation}")
        lines.append("")

    for name in order:
        spec = models[name]
        try:
            emit_dataclass(
                name,
                spec.get("parent") or "SemanticModel",
                semantics[name],
                model_entries[name]["fields"],
                [entry["chart"] for entry in model_entries[name]["chart_fields"]],
                projection=False,
            )
        except ValueError as exc:
            raise ValueError(f"model {name}: {exc}") from exc

    for name, spec in projection_entries.items():
        try:
            emit_dataclass(
                name,
                "SemanticModel",
                spec["semantics"],
                spec["fields"],
                spec["charts"],
                projection=True,
            )
        except ValueError as exc:
            raise ValueError(f"projection {name}: {exc}") from exc

    for relation_name, spec in relation_specs.items():
        signature = ", ".join(spec["signature"])
        if len(spec["signature"]) == 1:
            signature += ","
        kwargs = ""
        if spec["operand_names"]:
            kwargs += f", operand_names={tuple(spec['operand_names'])!r}"
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
