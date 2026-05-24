"""Generate a Pydantic schema package from `occid/lib/schema/core`.

Usage:
    python generate_pydantic.py
    python generate_pydantic.py --output-dir schema
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode
from yaml.tokens import AliasToken, AnchorToken, FlowMappingStartToken, FlowSequenceStartToken, TagToken


SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = SCRIPT_DIR / "lib" / "schema" / "core"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "schema"
TEMPLATE_DIR = SCRIPT_DIR / "lib" / "templates" / "pydantic"

PRIMITIVE_TYPES = {
    "string": "str",
    "int": "int",
    "int8": "int",
    "int16": "int",
    "int32": "int",
    "int64": "int",
    "uint8": "int",
    "uint16": "int",
    "uint32": "int",
    "uint64": "int",
    "float": "float",
    "bool": "bool",
    "bytes": "bytes",
    "any": "Any",
}

TYPE_KEYWORDS = {"list", "map", "tuple"}
TOP_LEVEL_KEYS = {"version", "type", "name", "description", "tags", "root", "branches", "enums", "maps", "models"}
MAP_KEYS = {"type", "value"}
MODEL_KEYS = {"parent", "fields", "variants"}
YAML_FORBIDDEN_TOKENS = {AliasToken, AnchorToken, FlowMappingStartToken, FlowSequenceStartToken, TagToken}


class SchemaError(RuntimeError):
    pass


@dataclass
class TypeNode:
    kind: str
    name: str | None = None
    args: list["TypeNode"] = field(default_factory=list)


@dataclass
class EnumValue:
    name: str
    value: int | str | None


@dataclass
class EnumDef:
    name: str
    values: list[EnumValue]


@dataclass
class FieldDef:
    name: str
    type_node: TypeNode
    optional: bool
    const: bool
    default: object = None
    has_default: bool = False


@dataclass
class ModelDef:
    name: str
    parent: str | None
    fields: list[FieldDef]


@dataclass
class MappingDef:
    name: str
    key_type: str
    value_type: str
    entries: dict


@dataclass
class ModuleDef:
    name: str
    path: Path
    enums: list[EnumDef]
    models: list[ModelDef]
    maps: list[MappingDef]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema-dir", type=Path, default=SCHEMA_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text().rstrip()


def validate_yaml_node(path: Path, node: ScalarNode | SequenceNode | MappingNode) -> None:
    if type(node) == MappingNode:
        keys: set[str] = set()
        for key_node, value_node in node.value:
            if type(key_node) != ScalarNode:
                raise SchemaError(f"mapping keys must be scalars in {path}")
            if key_node.value in keys:
                raise SchemaError(f"duplicate key {key_node.value!r} in {path}")
            keys.add(key_node.value)
            validate_yaml_node(path, key_node)
            validate_yaml_node(path, value_node)
        return

    if type(node) == SequenceNode:
        for value_node in node.value:
            validate_yaml_node(path, value_node)
        return

    if type(node) != ScalarNode:
        raise SchemaError(f"unsupported YAML node in {path}")


def validate_yaml_subset(path: Path, text: str) -> None:
    if "\t" in text:
        raise SchemaError(f"tabs are not allowed in {path}")
    for token in yaml.scan(text):
        if type(token) in YAML_FORBIDDEN_TOKENS:
            raise SchemaError(f"unsupported YAML token {type(token).__name__} in {path}")
    node = yaml.compose(text)
    validate_yaml_node(path, node)


def split_default(field_text: str) -> tuple[str, str | None]:
    depth = 0
    for index, char in enumerate(field_text):
        if char in "[(":
            depth += 1
        elif char in "])":
            depth -= 1
        elif char == "=" and depth == 0:
            return field_text[:index].rstrip(), field_text[index + 1 :].strip()
    return field_text.strip(), None


def strip_prefix(text: str, prefix: str) -> tuple[bool, str]:
    if text.startswith(prefix):
        return True, text[len(prefix) :].strip()
    return False, text


class TypeParser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def parse(self) -> TypeNode:
        node = self.parse_union()
        self.skip_ws()
        if self.pos != len(self.text):
            raise SchemaError(f"unexpected trailing type text: {self.text!r}")
        return node

    def parse_union(self) -> TypeNode:
        nodes = [self.parse_atom()]
        while True:
            self.skip_ws()
            if not self.consume("|"):
                break
            nodes.append(self.parse_atom())
        if len(nodes) == 1:
            return nodes[0]
        return TypeNode(kind="union", args=nodes)

    def parse_atom(self) -> TypeNode:
        self.skip_ws()
        if self.consume("("):
            node = self.parse_union()
            self.skip_ws()
            self.expect(")")
            return node

        name = self.parse_name()
        self.skip_ws()
        if not self.consume("["):
            return TypeNode(kind="name", name=name)

        args = [self.parse_union()]
        while True:
            self.skip_ws()
            if not self.consume(","):
                break
            args.append(self.parse_union())
        self.skip_ws()
        self.expect("]")
        return TypeNode(kind=name, args=args)

    def parse_name(self) -> str:
        self.skip_ws()
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == "_"):
            self.pos += 1
        if start == self.pos:
            raise SchemaError(f"expected type name in {self.text!r}")
        return self.text[start:self.pos]

    def skip_ws(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def consume(self, token: str) -> bool:
        self.skip_ws()
        if self.text.startswith(token, self.pos):
            self.pos += len(token)
            return True
        return False

    def expect(self, token: str) -> None:
        if not self.consume(token):
            raise SchemaError(f"expected {token!r} in {self.text!r}")


def parse_enum_value(raw_entry: str) -> EnumValue:
    if "=" not in raw_entry:
        return EnumValue(name=raw_entry.strip(), value=None)

    name, value_text = [part.strip() for part in raw_entry.split("=", 1)]
    if value_text.startswith(("'", '"')):
        return EnumValue(name=name, value=yaml.safe_load(value_text))
    return EnumValue(name=name, value=int(value_text))


def parse_enum(name: str, entries: list[str]) -> EnumDef:
    return EnumDef(name=name, values=[parse_enum_value(entry) for entry in entries])


def parse_field(name: str, spec: str | dict) -> FieldDef:
    if type(spec) == dict:
        if "required" in spec:
            raise SchemaError(f"required is not allowed on field {name}; use optional in the type")
        if "default" in spec and "value" in spec:
            raise SchemaError(f"default and value may not both appear on field {name}")
        type_text = spec["type"].strip()
        has_default = "value" in spec or "default" in spec
        default = spec["value"] if "value" in spec else spec.get("default")
    else:
        type_text, default = split_default(spec)
        has_default = default is not None
        if default in {"[]", "{}"}:
            raise SchemaError(f"list/map/object defaults must use expanded form on field {name}")
        if has_default:
            default = yaml.safe_load(default)

    optional, type_text = strip_prefix(type_text, "optional ")
    const, type_text = strip_prefix(type_text, "const ")
    if optional and const:
        raise SchemaError(f"optional const is invalid on field {name}")
    if type_text.startswith("optional ") or type_text.startswith("const "):
        raise SchemaError(f"invalid repeated type qualifier on field {name}")
    return FieldDef(
        name=name,
        type_node=TypeParser(type_text).parse(),
        optional=optional,
        const=const,
        default=default,
        has_default=has_default,
    )


def parse_model(name: str, spec: dict) -> ModelDef:
    unknown_keys = sorted(set(spec) - MODEL_KEYS)
    if unknown_keys:
        raise SchemaError(f"unknown model keys {unknown_keys} on {name}")
    if "variants" in spec:
        raise SchemaError(f"variants are specified by the IDL but not implemented by the compiler yet on {name}")
    return ModelDef(
        name=name,
        parent=spec.get("parent"),
        fields=[parse_field(field_name, field_spec) for field_name, field_spec in (spec.get("fields") or {}).items()],
    )


def parse_mapping(name: str, spec: dict) -> MappingDef:
    unknown_keys = sorted(set(spec) - MAP_KEYS)
    if unknown_keys:
        raise SchemaError(f"unknown map keys {unknown_keys} on {name}")
    type_node = TypeParser(spec["type"]).parse()
    if type_node.kind != "map":
        raise SchemaError(f"mapping {name} type must be map[K, V]")
    return MappingDef(
        name=name,
        key_type=type_node.args[0].name,
        value_type=type_node.args[1].name,
        entries=spec["value"],
    )


def load_modules(schema_dir: Path) -> list[ModuleDef]:
    modules: list[ModuleDef] = []
    paths = sorted(schema_dir.rglob("*.schema.yaml"))
    schema_names: set[str] = set()
    schema_data: list[tuple[Path, dict]] = []
    for path in paths:
        text = path.read_text()
        validate_yaml_subset(path, text)
        data = yaml.safe_load(text)
        unknown_keys = sorted(set(data) - TOP_LEVEL_KEYS)
        if unknown_keys:
            raise SchemaError(f"unknown top-level keys {unknown_keys} in {path}")
        for key in ("version", "type", "name", "description", "tags"):
            if key not in data:
                raise SchemaError(f"missing {key} in {path}")
        if data["type"] != "schema":
            raise SchemaError(f"type must be schema in {path}")
        expected_name = path.stem.replace(".schema", "")
        if data["name"] != expected_name:
            raise SchemaError(f"name {data['name']} does not match schema id {expected_name}")
        if data["name"] in schema_names:
            raise SchemaError(f"duplicate schema id {data['name']} in {path}")
        schema_names.add(data["name"])
        schema_data.append((path, data))

    branch_graph: dict[str, set[str]] = {}
    branch_parent: dict[str, str] = {}
    root_by_name: dict[str, str] = {}
    rootless_schema_names = [data["name"] for path, data in schema_data if not data.get("root")]
    if len(rootless_schema_names) != 1:
        raise SchemaError(f"expected one schema with no root, found {rootless_schema_names}")
    tree_root = rootless_schema_names[0]
    for path, data in schema_data:
        schema_name = data["name"]
        if schema_name != tree_root and not data.get("root"):
            raise SchemaError(f"missing root in {path}")
        if data.get("root") and data["root"] not in schema_names:
            raise SchemaError(f"unknown root {data['root']} in {path}")
        if data.get("root"):
            root_by_name[schema_name] = data["root"]
        branch_graph[schema_name] = set(data.get("branches") or [])
        for branch_name in data.get("branches") or []:
            if branch_name not in schema_names:
                raise SchemaError(f"unknown branch {branch_name} in {path}")
            if branch_name in branch_parent:
                raise SchemaError(f"branch {branch_name} has multiple roots: {branch_parent[branch_name]}, {schema_name}")
            branch_parent[branch_name] = schema_name
        modules.append(
            ModuleDef(
                name=path.stem.replace(".schema", ""),
                path=path,
                enums=[parse_enum(name, entries) for name, entries in (data.get("enums") or {}).items()],
                models=[parse_model(name, spec) for name, spec in (data.get("models") or {}).items()],
                maps=[parse_mapping(name, spec) for name, spec in (data.get("maps") or {}).items()],
            )
        )
    checking: set[str] = set()
    checked: set[str] = set()
    for name in schema_names:
        stack: list[tuple[str, bool]] = [(name, False)]
        while stack:
            current, leaving = stack.pop()
            if leaving:
                checking.remove(current)
                checked.add(current)
                continue
            if current in checked:
                continue
            if current in checking:
                raise SchemaError(f"branches graph contains a cycle at {current}")
            checking.add(current)
            stack.append((current, True))
            for branch_name in branch_graph[current]:
                stack.append((branch_name, False))
    for name, root in root_by_name.items():
        if branch_parent.get(name) != root:
            raise SchemaError(f"root {root} does not branch to {name}")
    return modules


def build_symbol_index(modules: list[ModuleDef]) -> dict[str, str]:
    symbols = {"OCCIDModel": "common", "IntEnum": "common"}
    for module in modules:
        for enum_def in module.enums:
            if enum_def.name in symbols:
                raise SchemaError(f"duplicate symbol {enum_def.name} in {module.path}")
            symbols[enum_def.name] = module.name
        for model_def in module.models:
            if model_def.name in symbols:
                raise SchemaError(f"duplicate symbol {model_def.name} in {module.path}")
            symbols[model_def.name] = module.name
    return symbols


def build_enum_members(modules: list[ModuleDef]) -> dict[str, set[str]]:
    enum_members: dict[str, set[str]] = {}
    for module in modules:
        for enum_def in module.enums:
            members: set[str] = set()
            for value in enum_def.values:
                if value.name in members:
                    raise SchemaError(f"duplicate enum member {enum_def.name}.{value.name} in {module.path}")
                members.add(value.name)
            enum_members[enum_def.name] = members
    return enum_members


def collect_type_refs(node: TypeNode) -> set[str]:
    if node.kind == "name":
        if node.name in PRIMITIVE_TYPES or node.name in TYPE_KEYWORDS:
            return set()
        return {node.name}
    refs: set[str] = set()
    for arg in node.args:
        refs.update(collect_type_refs(arg))
    return refs


def validate_schema(modules: list[ModuleDef], symbol_index: dict[str, str], enum_members: dict[str, set[str]]) -> None:
    for module in modules:
        for mapping_def in module.maps:
            for type_name in (mapping_def.key_type, mapping_def.value_type):
                if type_name not in PRIMITIVE_TYPES and type_name not in symbol_index:
                    raise SchemaError(f"unknown mapping type {type_name} in {module.path}:{mapping_def.name}")
            if mapping_def.key_type in enum_members:
                for key in mapping_def.entries:
                    if key not in enum_members[mapping_def.key_type]:
                        raise SchemaError(f"invalid mapping key {mapping_def.key_type}.{key} in {module.path}:{mapping_def.name}")
        for model_def in module.models:
            if model_def.parent and model_def.parent not in symbol_index:
                raise SchemaError(f"unknown parent {model_def.parent} in {module.path}")
            for field_def in model_def.fields:
                unknown_refs = sorted(ref for ref in collect_type_refs(field_def.type_node) if ref not in symbol_index)
                if unknown_refs:
                    raise SchemaError(f"unknown type refs {unknown_refs} in {module.path}:{model_def.name}.{field_def.name}")
                if field_def.const and not field_def.has_default:
                    raise SchemaError(f"const field without value in {module.path}:{model_def.name}.{field_def.name}")
                type_name = field_def.type_node.name if field_def.type_node.kind == "name" else None
                if type_name in enum_members and type(field_def.default) == str and field_def.default not in enum_members[type_name]:
                    raise SchemaError(
                        f"invalid enum default {type_name}.{field_def.default} in {module.path}:{model_def.name}.{field_def.name}"
                    )


def python_type_expr(node: TypeNode) -> str:
    if node.kind == "name":
        return PRIMITIVE_TYPES.get(node.name, node.name)
    if node.kind == "list":
        return f"list[{python_type_expr(node.args[0])}]"
    if node.kind == "map":
        return f"dict[{python_type_expr(node.args[0])}, {python_type_expr(node.args[1])}]"
    if node.kind == "tuple":
        return f"tuple[{', '.join(python_type_expr(arg) for arg in node.args)}]"
    if node.kind == "union":
        return " | ".join(python_type_expr(arg) for arg in node.args)
    raise SchemaError(f"unsupported type node {node.kind}")


def field_annotation(field_def: FieldDef) -> str:
    python_type = python_type_expr(field_def.type_node)
    if field_def.const and field_def.default is not None and field_def.type_node.kind == "name":
        if field_def.type_node.name in {"string", "int", "float", "bool"}:
            return f"Literal[{python_default_literal(field_def.default)}]"
    if field_def.optional:
        if field_def.type_node.kind == "union":
            return f"({python_type}) | None"
        return f"{python_type} | None"
    return python_type


def python_default_literal(value: object) -> str:
    if value is True:
        return "True"
    if value is False:
        return "False"
    if type(value) == str:
        return repr(value)
    if type(value) in {int, float}:
        return repr(value)
    if value == "true":
        return "True"
    if value == "false":
        return "False"
    if value == "[]":
        return "[]"
    if value == "{}":
        return "{}"
    return repr(value) if type(value) != str else value


def enum_default_expr(type_name: str, default: str, enum_members: dict[str, set[str]]) -> str:
    if default not in enum_members[type_name]:
        raise SchemaError(f"invalid enum default {type_name}.{default}")
    return f"{type_name}.{default}"


def field_assignment(field_def: FieldDef, enum_members: dict[str, set[str]]) -> str:
    annotation = field_annotation(field_def)

    if field_def.const:
        type_name = field_def.type_node.name if field_def.type_node.kind == "name" else None
        if type_name in enum_members:
            default_expr = enum_default_expr(type_name, field_def.default, enum_members)
        else:
            default_expr = python_default_literal(field_def.default)
        return f"{annotation} = Field(default={default_expr}, frozen=True)"

    if not field_def.has_default:
        if field_def.optional:
            return f"{annotation} = None"
        return annotation

    if field_def.default is None:
        return f"{annotation} = None"

    if type(field_def.default) == list:
        if field_def.type_node.kind != "list":
            raise SchemaError(f"list default on non-list field {field_def.name}")
        if not field_def.default:
            return f"{annotation} = Field(default_factory=list)"
        return f"{annotation} = Field(default_factory=lambda: {repr(field_def.default)})"

    if type(field_def.default) == dict:
        if field_def.type_node.kind == "map":
            if not field_def.default:
                return f"{annotation} = Field(default_factory=dict)"
            return f"{annotation} = Field(default_factory=lambda: {repr(field_def.default)})"
        if field_def.type_node.kind == "name" and field_def.type_node.name not in PRIMITIVE_TYPES:
            if not field_def.default:
                return f"{annotation} = Field(default_factory={field_def.type_node.name})"
            return f"{annotation} = Field(default_factory=lambda: {repr(field_def.default)})"
        raise SchemaError(f"object default on unsupported field {field_def.name}")

    if field_def.default == "[]":
        if field_def.type_node.kind != "list":
            raise SchemaError(f"list default on non-list field {field_def.name}")
        return f"{annotation} = Field(default_factory=list)"

    if field_def.default == "{}":
        if field_def.type_node.kind == "map":
            return f"{annotation} = Field(default_factory=dict)"
        if field_def.type_node.kind == "name" and field_def.type_node.name not in PRIMITIVE_TYPES:
            return f"{annotation} = Field(default_factory={field_def.type_node.name})"
        raise SchemaError(f"object default on unsupported field {field_def.name}")

    type_name = field_def.type_node.name if field_def.type_node.kind == "name" else None
    if type_name in enum_members and type(field_def.default) == str:
        default_expr = enum_default_expr(type_name, field_def.default, enum_members)
    else:
        default_expr = python_default_literal(field_def.default)
    return f"{annotation} = {default_expr}"


def enum_base(enum_def: EnumDef) -> str:
    has_string_values = any(type(value.value) == str for value in enum_def.values if value.value is not None)
    return "str, Enum" if has_string_values else "IntEnum"


def render_enum_block(enum_def: EnumDef) -> str:
    lines = [f"class {enum_def.name}({enum_base(enum_def)}):"]
    next_value: int | None = None
    for index, value in enumerate(enum_def.values):
        if type(value.value) == str:
            lines.append(f"    {value.name} = {repr(value.value)}")
            continue
        if type(value.value) == int:
            lines.append(f"    {value.name} = {value.value}")
            next_value = value.value + 1
            continue
        if index == 0 or next_value is None:
            raise SchemaError(f"first enum member {enum_def.name}.{value.name} must have an explicit integer value")
        lines.append(f"    {value.name} = auto()")
        next_value += 1
    return "\n".join(lines)


def model_type_refs(model_def: ModelDef) -> set[str]:
    refs: set[str] = set()
    if model_def.parent:
        refs.add(model_def.parent)
    for field_def in model_def.fields:
        refs.update(collect_type_refs(field_def.type_node))
    return refs


def runtime_type_refs(model_def: ModelDef, enum_members: dict[str, set[str]]) -> set[str]:
    refs: set[str] = set()
    if model_def.parent:
        refs.add(model_def.parent)
    for field_def in model_def.fields:
        if field_def.type_node.kind == "name" and field_def.type_node.name in enum_members and field_def.default is not None:
            refs.add(field_def.type_node.name)
        if field_def.type_node.kind == "name" and field_def.default == "{}":
            refs.add(field_def.type_node.name)
        if field_def.type_node.kind == "name" and type(field_def.default) == dict:
            refs.add(field_def.type_node.name)
    return refs


def module_imports(module: ModuleDef, symbol_index: dict[str, str], enum_members: dict[str, set[str]]) -> list[str]:
    imports_by_module: dict[str, set[str]] = {}
    for mapping_def in module.maps:
        for ref in (mapping_def.key_type, mapping_def.value_type):
            if ref in PRIMITIVE_TYPES:
                continue
            ref_module = symbol_index[ref]
            if ref_module in {module.name, "common"}:
                continue
            imports_by_module.setdefault(ref_module, set()).add(ref)
    for model_def in module.models:
        for ref in sorted(runtime_type_refs(model_def, enum_members)):
            ref_module = symbol_index[ref]
            if ref_module in {module.name, "common"}:
                continue
            imports_by_module.setdefault(ref_module, set()).add(ref)
    lines = []
    for ref_module in sorted(imports_by_module):
        symbols = ", ".join(sorted(imports_by_module[ref_module]))
        lines.append(f"from .{ref_module} import {symbols}")
    return lines


def render_model_block(model_def: ModelDef, enum_members: dict[str, set[str]]) -> str:
    parent = model_def.parent or "OCCIDModel"
    lines = [f"class {model_def.name}({parent}):"]
    for field_def in model_def.fields:
        lines.append(f"    {field_def.name}: {field_assignment(field_def, enum_members)}")
    return "\n".join(lines)


def mapping_key_literal(key: object, key_type: str, enum_members: dict[str, set[str]]) -> str:
    if key_type in enum_members:
        return f"{key_type}.{key}"
    return repr(key)


def mapping_value_literal(value: object, value_type: str, enum_members: dict[str, set[str]]) -> str:
    if value_type in enum_members:
        return f"{value_type}.{value}"
    return repr(value)


def render_mapping_block(mapping_def: MappingDef, enum_members: dict[str, set[str]]) -> str:
    lines = [f"{mapping_def.name}: dict[{python_type_expr(TypeParser(mapping_def.key_type).parse())}, {python_type_expr(TypeParser(mapping_def.value_type).parse())}] = {{"]
    for key, value in mapping_def.entries.items():
        key_expr = mapping_key_literal(key, mapping_def.key_type, enum_members)
        value_expr = mapping_value_literal(value, mapping_def.value_type, enum_members)
        lines.append(f"    {key_expr}: {value_expr},")
    lines.append("}")
    return "\n".join(lines)


def render_common_runtime() -> str:
    sections = [load_template("common_header.py"), load_template("common_intenum.py"), load_template("common_runtime.py")]
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def render_module(module: ModuleDef, symbol_index: dict[str, str], enum_members: dict[str, set[str]]) -> str:
    sections = [load_template("module_header.py")]
    imports = module_imports(module, symbol_index, enum_members)
    if imports:
        sections.append("\n".join(imports))
    if module.enums:
        sections.append("### Enums")
        sections.append("\n\n".join(render_enum_block(enum_def) for enum_def in module.enums))
    if module.maps:
        sections.append("### Mappings")
        sections.append("\n\n".join(render_mapping_block(mapping_def, enum_members) for mapping_def in module.maps))
    if module.models:
        sections.append("### Models")
        sections.append("\n\n".join(render_model_block(model_def, enum_members) for model_def in module.models))
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def module_dependency_graph(
    modules: list[ModuleDef], symbol_index: dict[str, str], enum_members: dict[str, set[str]]
) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for module in modules:
        refs: set[str] = set()
        for mapping_def in module.maps:
            for ref in (mapping_def.key_type, mapping_def.value_type):
                if ref in symbol_index and symbol_index[ref] != module.name:
                    refs.add(ref)
        for model_def in module.models:
            for ref in runtime_type_refs(model_def, enum_members):
                ref_module = symbol_index[ref]
                if ref_module not in {module.name, "common"}:
                    refs.add(ref_module)
        graph[module.name] = refs
    return graph


def topo_sort_modules(modules: list[ModuleDef], graph: dict[str, set[str]]) -> list[str]:
    remaining = {module.name for module in modules}
    ordered: list[str] = []
    while remaining:
        ready = sorted(name for name in remaining if graph[name].issubset(set(ordered)))
        if not ready:
            cycle = ", ".join(sorted(remaining))
            raise SchemaError(f"cyclic module dependencies: {cycle}")
        ordered.extend(ready)
        remaining.difference_update(ready)
    return ordered


def render_init(module_names: list[str]) -> str:
    lines = ["from .common import *"]
    lines.extend(f"from .{name} import *" for name in module_names)
    lines.extend(
        [
            "",
            "for _model in [obj for obj in list(globals().values()) if OCCIDModel in getattr(obj, \"__mro__\", ()) and obj is not OCCIDModel]:",
            "    _model.model_rebuild(_types_namespace=globals())",
        ]
    )
    lines.append("")
    lines.append('__all__ = [name for name in globals() if not name.startswith("_")]')
    return "\n".join(lines) + "\n"


def write_package(output_dir: Path, modules: list[ModuleDef], symbol_index: dict[str, str], enum_members: dict[str, set[str]]) -> None:
    graph = module_dependency_graph(modules, symbol_index, enum_members)
    ordered_names = topo_sort_modules(modules, graph)
    module_map = {module.name: module for module in modules}

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    (output_dir / "common.py").write_text(render_common_runtime())

    for module_name in ordered_names:
        module = module_map[module_name]
        (output_dir / f"{module_name}.py").write_text(render_module(module, symbol_index, enum_members))

    (output_dir / "__init__.py").write_text(render_init(ordered_names))


def main() -> None:
    args = parse_args()
    modules = load_modules(args.schema_dir)
    symbol_index = build_symbol_index(modules)
    enum_members = build_enum_members(modules)
    validate_schema(modules, symbol_index, enum_members)
    write_package(args.output_dir, modules, symbol_index, enum_members)
    print(f"schema_dir={args.schema_dir}")
    print(f"output_dir={args.output_dir}")
    print(f"module_count={len(modules)}")


if __name__ == "__main__":
    main()
