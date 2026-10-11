"""Read runtime declarations. No Python or wire types are generated."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any

import yaml

SECTIONS = ("factors", "axes", "aliases", "charts", "expressions", "relations", "mappings", "vocabularies")
CONSTRAINT_KEYS = {"description", "applies", "requires", "disjoint", "excludes"}
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PRODUCT_SPLIT = re.compile(r"\s*[*×]\s*")
COORDINATE = re.compile(r"^(?P<optional>optional )?(?P<type>float|int|string|bool|bytes)(?:\[(?P<unit>[^\]]+)\])?$")
EQUATION = re.compile(r"^(?P<quantity>[\w.]+)\((?P<of>\w+)\)\s*=\s*(?P<equals>\w+)$")


class DefinitionLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise ValueError(f"line {key_node.start_mark.line + 1}: duplicate YAML key {key!r}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def load_definitions(path: str | Path) -> dict[str, Any]:
    return yaml.load(Path(path).read_text(), Loader=DefinitionLoader)


def identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f"{context}: expected identifier, got {value!r}; quote YAML boolean tokens")
    return value


def mapping(value: Any, context: str) -> dict:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{context}: expected mapping with text keys")
    return value


def keys(value: dict, allowed: set[str], context: str) -> None:
    unknown = value.keys() - allowed
    if unknown:
        raise ValueError(f"{context}: unknown declaration keys {sorted(unknown)}")


def product_terms(raw: Any) -> list[str]:
    if raw is None:
        return []
    items = [raw] if isinstance(raw, str) else raw
    if not isinstance(items, list) or any(not isinstance(item, str) for item in items):
        raise ValueError(f"expected a semantic product, got {raw!r}")
    result = []
    for item in items:
        parts = PRODUCT_SPLIT.split(item)
        if any(not part.strip() for part in parts):
            raise ValueError(f"empty semantic factor in {item!r}")
        result.extend(part.strip() for part in parts)
    return list(dict.fromkeys(result))


def validate_terms(raw, context, *, known):
    terms = product_terms(raw)
    for term in terms:
        if term not in known:
            raise ValueError(f"{context}: unknown semantic term {term!r}")
    return terms


def resolve_alias(name, trail=(), *, raw_aliases, known, aliases):
    if name in trail:
        raise ValueError(f"alias cycle: {' -> '.join((*trail, name))}")
    if name not in aliases:
        result = []
        for term in validate_terms(raw_aliases[name], f"alias {name}", known=known):
            result.extend(resolve_alias(term, (*trail, name), raw_aliases=raw_aliases, known=known, aliases=aliases) if term in raw_aliases else [term])
        aliases[name] = list(dict.fromkeys(result))
    return aliases[name]


def region(raw, context, *, known, aliases, axis_names):
    if raw is None or type(raw) is bool:
        return raw
    if isinstance(raw, (str, list)):
        parts = []
        if isinstance(raw, str):
            for term in validate_terms(raw, context, known=known):
                parts.extend(aliases.get(term, [term]))
        else:
            return {"all": [region(item, context, known=known, aliases=aliases, axis_names=axis_names) for item in raw]}
        return {"all": parts}
    raw = mapping(raw, context)
    if len(raw) != 1:
        raise ValueError(f"{context}: region needs exactly one operator")
    operator, value = next(iter(raw.items()))
    if operator in ("all", "any"):
        if not isinstance(value, list):
            raise ValueError(f"{context}: {operator} needs a list")
        return {operator: [region(item, context, known=known, aliases=aliases, axis_names=axis_names) for item in value]}
    if operator in ("not", "term"):
        return {"not": region(value, context, known=known, aliases=aliases, axis_names=axis_names)} if operator == "not" else region(value, context, known=known, aliases=aliases, axis_names=axis_names)
    if operator == "axis" and value in axis_names:
        return raw
    if operator == "const" and type(value) is bool:
        return raw
    raise ValueError(f"{context}: invalid region {raw!r}")


def constraints(declaration, context, *, known, aliases, axis_names):
    for key in ("applies", "requires"):
        if key in declaration:
            declaration[key] = region(declaration[key], f"{context} {key}", known=known, aliases=aliases, axis_names=axis_names)
    for key in ("disjoint", "excludes"):
        if key in declaration:
            if not isinstance(declaration[key], list):
                raise ValueError(f"{context} {key}: expected list")
            declaration[key] = [region(item, f"{context} {key}", known=known, aliases=aliases, axis_names=axis_names) for item in declaration[key]]


def expand(raw, context, *, known, aliases):
    return list(dict.fromkeys(part for term in validate_terms(raw, context, known=known) for part in aliases.get(term, [term])))


def resolve_expression(name, trail=(), *, raw_expressions):
    if name in trail:
        raise ValueError(f"expression scheme cycle: {' -> '.join((*trail, name))}")
    if name not in raw_expressions:
        raise ValueError(f"unknown expression scheme {name!r}")
    item = mapping(raw_expressions[name], f"expression {name}")
    keys(item, {"description", "of", "factors", "binds", "given", "sought", "equations", "words"}, f"expression {name}")
    if "of" in item:
        identifier(item["of"], f"expression {name} scheme")
    base = resolve_expression(item["of"], (*trail, name), raw_expressions=raw_expressions) if item.get("of") else {}
    return {**base, **item, "binds": product_terms(base.get("binds")) + product_terms(item.get("binds"))}


def expression(name, item, bindings, word_names, *, known, aliases, expressions, words):
    if name in expressions:
        raise ValueError(f"duplicate expression {name!r}")
    given = {role: expand(value, f"expression {name} {role}", known=known, aliases=aliases) for role, value in mapping(item.get("given", {}), name).items()}
    sought = {role: expand(value, f"expression {name} {role}", known=known, aliases=aliases) for role, value in mapping(item.get("sought", {}), name).items()}
    if given.keys() & sought.keys():
        raise ValueError(f"expression {name}: duplicate variable")
    for role in (*given, *sought):
        identifier(role, f"expression {name} variable")
    equations = []
    for text in item.get("equations", []):
        match = EQUATION.fullmatch(text.strip()) if isinstance(text, str) else None
        if not match:
            raise ValueError(f"expression {name}: invalid equation {text!r}")
        equation = match.groupdict()
        validate_terms(equation["quantity"], f"expression {name} equation", known=known)
        if equation["of"] not in given or equation["equals"] not in {*given, *sought}:
            raise ValueError(f"expression {name}: equation references undeclared variable")
        equations.append(equation)
    for word in word_names:
        if not isinstance(word, str) or len(word.split(".")) != 2:
            raise ValueError(f"expression {name}: word must be Vocabulary.MEMBER")
        for part in word.split("."):
            identifier(part, "word")
        if word in words:
            raise ValueError(f"word {word!r} names more than one expression")
        words[word] = name
    expressions[name] = {"factors": expand(product_terms(item.get("factors")) + bindings, name, known=known, aliases=aliases), "given": given, "sought": sought, "equations": equations, "words": word_names}


def prepare(spec: dict[str, Any]) -> dict[str, Any]:
    """Validate declaration structure and resolve aliases and expression forms."""
    spec = deepcopy(mapping(spec, "definitions"))
    keys(spec, set(SECTIONS) | {"version", "description"}, "definitions")
    if spec.get("version", 2) != 2:
        raise ValueError("expected version 2 semantic definitions")
    data = {section: mapping(spec.get(section, {}), section) for section in SECTIONS}
    declared = set()
    for section in ("factors", "axes", "aliases", "expressions", "relations", "vocabularies"):
        for name in data[section]:
            identifier(name, section)
            if name in declared:
                raise ValueError(f"duplicate declaration {name!r}")
            declared.add(name)

    axis_names = set(data["axes"])
    known = set(data["factors"]) | set(data["aliases"])
    for name, raw in data["axes"].items():
        axis = mapping(raw, f"axis {name}")
        keys(axis, CONSTRAINT_KEYS | {"cardinality", "values"}, f"axis {name}")
        if axis.get("cardinality", "many") not in ("one", "many"):
            raise ValueError(f"axis {name}: cardinality must be one or many")
        values = axis.get("values", [])
        if isinstance(values, list):
            if len(values) != len(set(identifier(value, f"axis {name} value") for value in values)):
                raise ValueError(f"axis {name}: duplicate value")
            values = {value: {} for value in values}
        values = mapping(values, f"axis {name} values")
        for value, declaration in values.items():
            identifier(value, f"axis {name} value")
            declaration = {} if declaration is None else mapping(declaration, f"{name}.{value}")
            keys(declaration, CONSTRAINT_KEYS, f"{name}.{value}")
            values[value] = declaration
            known.add(f"{name}.{value}")
        data["axes"][name] = {**axis, "values": list(values), "value_meta": values}

    raw_aliases = data["aliases"]
    aliases = {}

    for name in data["aliases"]:
        resolve_alias(name, raw_aliases=raw_aliases, known=known, aliases=aliases)
    data["aliases"] = aliases

    for name, raw in data["factors"].items():
        factor = {} if raw is None else mapping(raw, f"factor {name}")
        keys(factor, CONSTRAINT_KEYS | {"implies"}, f"factor {name}")
        constraints(factor, name, known=known, aliases=aliases, axis_names=axis_names)
        if "implies" in factor:
            factor["implies"] = region(factor["implies"], f"factor {name} implies", known=known, aliases=aliases, axis_names=axis_names)
        data["factors"][name] = factor
    for name, axis in data["axes"].items():
        constraints(axis, name, known=known, aliases=aliases, axis_names=axis_names)
        for value, declaration in axis["value_meta"].items():
            constraints(declaration, f"{name}.{value}", known=known, aliases=aliases, axis_names=axis_names)

    charts = []
    for display, raw in data["charts"].items():
        raw = mapping(raw, f"chart {display}")
        context = {}
        if "coords" in raw:
            keys(raw, {"coords", "context"}, f"chart {display}")
            context = mapping(raw.get("context", {}), f"chart {display} context")
            raw = mapping(raw["coords"], f"chart {display} coordinates")
        coordinates = []
        for name, declaration in raw.items():
            identifier(name, f"chart {display} coordinate")
            match = COORDINATE.fullmatch(declaration) if isinstance(declaration, str) else None
            if not match:
                raise ValueError(f"chart {display}: invalid primitive coordinate {name}: {declaration!r}")
            coordinates.append({"name": name, **match.groupdict()})
        charts.append({"display": display, "factors": expand(display, "chart", known=known, aliases=aliases), "coords": coordinates, "context": context})
    data["charts"] = charts

    raw_expressions = data["expressions"]
    expressions = {}
    words = {}

    for name in raw_expressions:
        item = resolve_expression(name, raw_expressions=raw_expressions)
        raw_words = item.get("words", [])
        if isinstance(raw_words, dict):
            for word, bindings in raw_words.items():
                if not isinstance(word, str):
                    raise ValueError("word must be text")
                expression(word.partition(".")[2], item, product_terms(item.get("binds")) + product_terms(bindings), [word], known=known, aliases=aliases, expressions=expressions, words=words)
        elif isinstance(raw_words, list):
            expression(name, item, product_terms(item.get("binds")), raw_words, known=known, aliases=aliases, expressions=expressions, words=words)
        else:
            raise ValueError(f"expression {name}: words must be a list or mapping")
    data["expressions"] = expressions
    data["word_expressions"] = words

    for name, raw in data["relations"].items():
        relation = mapping(raw, f"relation {name}")
        keys(relation, {"description", "operands", "specializes"}, name)
        operands = mapping(relation.get("operands", {}), f"relation {name} operands")
        if "specializes" in relation:
            identifier(relation["specializes"], f"relation {name} specialization")
        if not operands:
            raise ValueError(f"relation {name}: needs named operands")
        for role, value in operands.items():
            identifier(role, f"relation {name} role")
            operands[role] = expand(value, f"relation {name} {role}", known=known, aliases=aliases)

    for name, raw in data["mappings"].items():
        item = mapping(raw, f"mapping {name}")
        keys(item, {"description", "semantics", "fields", "context"}, f"mapping {name}")
        if "semantics" not in item:
            raise ValueError(f"mapping {name}: needs an explicit semantic product")
        item["semantics"] = expand(item.get("semantics"), f"mapping {name}", known=known, aliases=aliases)
        fields = mapping(item.get("fields", {}), f"mapping {name} fields")
        if any(not isinstance(value, str) or not value for value in fields.values()):
            raise ValueError(f"mapping {name}: source field names must be text")
        mapping(item.get("context", {}), f"mapping {name} context")
    for name, members in data["vocabularies"].items():
        members = mapping(members, f"vocabulary {name}")
        for member in members:
            identifier(member, f"vocabulary {name} member")
    return data
