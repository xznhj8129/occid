"""Generate the Pydantic runtime package from compiled ``occid.yaml``.

The authored hierarchy under ``lib/schema`` is consumed by ``compile_occid.py``.
This generator only sees the flat Type / Representation / Vocabulary contract.
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
MODULE_DIR = SCRIPT_DIR / "lib" / "schema" / "modules"
COMPILED_SCHEMA = SCRIPT_DIR / "occid.yaml"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "schema"
TEMPLATE_DIR = SCRIPT_DIR / "lib" / "templates" / "pydantic"
CORE_SCHEMA_MAX_PARTS = 3

PRIMITIVE_TYPES = {
    "string": "builtins.str",
    "int": "builtins.int",
    "int8": "builtins.int",
    "int16": "builtins.int",
    "int32": "builtins.int",
    "int64": "builtins.int",
    "uint8": "builtins.int",
    "uint16": "builtins.int",
    "uint32": "builtins.int",
    "uint64": "builtins.int",
    "float": "builtins.float",
    "bool": "builtins.bool",
    "bytes": "builtins.bytes",
    "any": "Any",
}

TYPE_KEYWORDS = {"list", "map", "tuple"}
TOP_LEVEL_KEYS = {
    "version",
    "type",
    "package",
    "description",
    "tags",
    "root",
    "requires",
    "extend_variants",
    "enums",
    "maps",
    "models",
}
MAP_KEYS = {"type", "value"}
COMPILED_TOP_LEVEL_KEYS = {"version", "type", "vocabulary", "types", "representations", "maps"}
# ``family`` is compiler-owned semantic metadata. The Pydantic generator accepts
# it in the flat contract but deliberately does not expose it on runtime models.
COMPILED_MODEL_KEYS = {"model_id", "package", "family", "description", "type", "fields"}
COMPILED_VOCABULARY_KEYS = {"package", "values"}
COMPILED_MAP_KEYS = {"package", "type", "value"}
MODEL_KEYS = {"description", "semantic_role", "parent", "type", "fields", "variants"}
MODEL_SEMANTIC_ROLES = {"concept", "type", "representation"}
YAML_FORBIDDEN_TOKENS = {AliasToken, AnchorToken, FlowMappingStartToken, FlowSequenceStartToken, TagToken}


class SchemaError(RuntimeError):
    pass


@dataclass
class TypeNode:
    kind: str
    name: str | None = None
    args: list["TypeNode"] = field(default_factory=list)
    semantic_args: list[str] = field(default_factory=list)
    size: int | None = None


@dataclass
class EnumValue:
    name: str
    value: int | str | None
    bitflag: bool = False


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
    description: str | None
    semantic_role: str | None
    parent: str | None
    value_type: TypeNode | None
    fields: list[FieldDef]
    variants: list[str]
    has_variants: bool
    model_id: int | None = None


@dataclass
class MappingDef:
    name: str
    key_type: str
    value_type: str
    entries: dict


@dataclass
class ModuleDef:
    doc_type: str
    name: str
    root: str | None
    description: str | None
    path: Path
    tags: list[str]
    requires: list[str]
    extend_variants: dict[str, list[str]]
    enums: list[EnumDef]
    models: list[ModelDef]
    maps: list[MappingDef]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=COMPILED_SCHEMA)
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


def parse_semantic_role(name: str, value: object, allowed: set[str]) -> str | None:
    if value is None:
        return None
    if type(value) != str or value not in allowed:
        raise SchemaError(f"invalid semantic_role {value!r} on {name}; expected one of {sorted(allowed)}")
    return value


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
        if self.consume("("):
            semantic_args = [self.parse_name()]
            while True:
                self.skip_ws()
                if not self.consume(","):
                    break
                semantic_args.append(self.parse_name())
            self.skip_ws()
            self.expect(")")
            return TypeNode(kind="semantic", name=name, semantic_args=semantic_args)

        if not self.consume("["):
            return TypeNode(kind="name", name=name)

        if name == "bytes":
            self.skip_ws()
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            if start == self.pos:
                raise SchemaError(f"bytes length must be a positive integer in {self.text!r}")
            size = int(self.text[start:self.pos])
            self.skip_ws()
            self.expect("]")
            if size <= 0:
                raise SchemaError(f"fixed bytes length must be positive in {self.text!r}")
            return TypeNode(kind="fixed_bytes", size=size)

        if name not in TYPE_KEYWORDS:
            raise SchemaError(f"type {name} does not take arguments in {self.text!r}")

        args = [self.parse_union()]
        while True:
            self.skip_ws()
            if not self.consume(","):
                break
            args.append(self.parse_union())
        self.skip_ws()
        self.expect("]")

        expected = {"list": 1, "map": 2}
        if name in expected and len(args) != expected[name]:
            raise SchemaError(f"{name} requires exactly {expected[name]} type argument(s) in {self.text!r}")
        if name == "tuple" and len(args) < 2:
            raise SchemaError(f"tuple requires at least two type arguments in {self.text!r}")
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
    if "<<" in value_text:
        left, right = [part.strip() for part in value_text.split("<<", 1)]
        return EnumValue(name=name, value=int(left) << int(right), bitflag=True)
    return EnumValue(name=name, value=int(value_text))


def parse_enum(name: str, entries: list[str]) -> EnumDef:
    if type(entries) != list:
        raise SchemaError(f"enum {name} values must be a list")
    for entry in entries:
        if type(entry) != str:
            raise SchemaError(f"enum {name} values must be strings")
    return EnumDef(
        name=name,
        values=[parse_enum_value(entry) for entry in entries],
    )


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
    if "description" in spec and type(spec["description"]) != str:
        raise SchemaError(f"description must be a string on {name}")
    semantic_role = parse_semantic_role(name, spec.get("semantic_role"), MODEL_SEMANTIC_ROLES)
    fields_spec = spec.get("fields") or {}
    if type(fields_spec) != dict:
        raise SchemaError(f"fields must be a mapping on {name}")
    if "type" in spec and "fields" in spec:
        raise SchemaError(f"model {name} may declare type or fields, not both")
    value_type = None
    if "type" in spec:
        if semantic_role != "representation":
            raise SchemaError(f"model-level type is only valid on a representation: {name}")
        type_text = spec["type"]
        if type(type_text) != str or not type_text.strip():
            raise SchemaError(f"model-level type must be a non-empty string on {name}")
        value_type = TypeParser(type_text.strip()).parse()
    has_variants = "variants" in spec
    variants = spec.get("variants") or []
    if type(variants) != list:
        raise SchemaError(f"variants must be a list on {name}")
    for variant_name in variants:
        if type(variant_name) != str:
            raise SchemaError(f"variants must be a list of model names on {name}")
    return ModelDef(
        name=name,
        description=spec.get("description"),
        semantic_role=semantic_role,
        parent=spec.get("parent"),
        value_type=value_type,
        fields=[parse_field(field_name, field_spec) for field_name, field_spec in fields_spec.items()],
        variants=variants,
        has_variants=has_variants,
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


def parse_document(path: Path) -> tuple[ModuleDef, dict]:
    text = path.read_text()
    validate_yaml_subset(path, text)
    data = yaml.safe_load(text)
    unknown_keys = sorted(set(data) - TOP_LEVEL_KEYS)
    if unknown_keys:
        raise SchemaError(f"unknown top-level keys {unknown_keys} in {path}")
    for key in ("version", "type", "package", "tags"):
        if key not in data:
            raise SchemaError(f"missing {key} in {path}")
    if data["type"] not in {"schema", "module"}:
        raise SchemaError(f"type must be schema or module in {path}")
    expected_package = path.stem.replace(".schema", "")
    if data["type"] == "schema" and data["package"] != expected_package:
        raise SchemaError(f"package {data['package']} does not match schema package {expected_package}")
    if type(data["tags"]) != list:
        raise SchemaError(f"tags must be a list in {path}")
    for tag in data["tags"]:
        if type(tag) != str:
            raise SchemaError(f"tags must be strings in {path}")

    requires = data.get("requires") or []
    if type(requires) != list:
        raise SchemaError(f"requires must be a list in {path}")
    for requirement in requires:
        if type(requirement) != str:
            raise SchemaError(f"requires must be strings in {path}")

    extend_variants = data.get("extend_variants") or {}
    if type(extend_variants) != dict:
        raise SchemaError(f"extend_variants must be a mapping in {path}")
    for parent_name, variant_names in extend_variants.items():
        if type(parent_name) != str or type(variant_names) != list:
            raise SchemaError(f"extend_variants must map model names to lists in {path}")
        for variant_name in variant_names:
            if type(variant_name) != str:
                raise SchemaError(f"extend_variants values must be model names in {path}")

    if data["type"] == "schema":
        for module_key in ("requires", "extend_variants"):
            if module_key in data:
                raise SchemaError(f"{module_key} is only valid on module files in {path}")
        if "description" in data:
            raise SchemaError(f"description belongs on the root model in {path}")
        if "root" not in data:
            raise SchemaError(f"missing root in {path}")
        if type(data["root"]) != str:
            raise SchemaError(f"root must be a model name in {path}")
    else:
        if "root" in data:
            raise SchemaError(f"root is only valid on schema files in {path}")
        if "description" in data and type(data["description"]) != str:
            raise SchemaError(f"description must be a string in {path}")

    return (
        ModuleDef(
            doc_type=data["type"],
            name=data["package"],
            root=data.get("root"),
            description=data.get("description"),
            path=path,
            tags=data["tags"],
            requires=requires,
            extend_variants=extend_variants,
            enums=[parse_enum(name, entries) for name, entries in (data.get("enums") or {}).items()],
            models=[parse_model(name, spec) for name, spec in (data.get("models") or {}).items()],
            maps=[parse_mapping(name, spec) for name, spec in (data.get("maps") or {}).items()],
        ),
        data,
    )



def load_compiled_schema(path: Path) -> list[ModuleDef]:
    """Load the flat runtime schema emitted by ``compile_occid.py``."""
    text = path.read_text()
    validate_yaml_subset(path, text)
    data = yaml.safe_load(text) or {}

    unknown_keys = sorted(set(data) - COMPILED_TOP_LEVEL_KEYS)
    if unknown_keys:
        raise SchemaError(f"unknown compiled-schema keys {unknown_keys} in {path}")
    if data.get("version") != 1:
        raise SchemaError(f"compiled OCCID schema version must be 1 in {path}")
    if data.get("type") != "occid":
        raise SchemaError(f"compiled schema type must be occid in {path}")

    modules: dict[str, ModuleDef] = {}

    def module_for(package: object) -> ModuleDef:
        if type(package) != str or not package:
            raise SchemaError(f"compiled entry has invalid package {package!r} in {path}")
        module = modules.get(package)
        if module is None:
            module = ModuleDef(
                doc_type="compiled",
                name=package,
                root=None,
                description=None,
                path=path,
                tags=[],
                requires=[],
                extend_variants={},
                enums=[],
                models=[],
                maps=[],
            )
            modules[package] = module
        return module

    vocabulary = data.get("vocabulary") or {}
    if type(vocabulary) != dict:
        raise SchemaError(f"vocabulary must be a mapping in {path}")
    for name, spec in vocabulary.items():
        if type(spec) != dict:
            raise SchemaError(f"compiled vocabulary {name} must be a mapping in {path}")
        unknown = sorted(set(spec) - COMPILED_VOCABULARY_KEYS)
        if unknown:
            raise SchemaError(f"unknown keys {unknown} on compiled vocabulary {name}")
        if "package" not in spec or "values" not in spec:
            raise SchemaError(f"compiled vocabulary {name} requires package and values")
        module_for(spec["package"]).enums.append(parse_enum(name, spec["values"]))

    compiled_model_ids: set[int] = set()

    for section_name, semantic_role in (("types", "type"), ("representations", "representation")):
        section = data.get(section_name) or {}
        if type(section) != dict:
            raise SchemaError(f"{section_name} must be a mapping in {path}")
        for name, spec in section.items():
            if type(spec) != dict:
                raise SchemaError(f"compiled {semantic_role} {name} must be a mapping in {path}")
            unknown = sorted(set(spec) - COMPILED_MODEL_KEYS)
            if unknown:
                raise SchemaError(f"unknown keys {unknown} on compiled {semantic_role} {name}")
            if "model_id" not in spec or "package" not in spec:
                raise SchemaError(f"compiled {semantic_role} {name} requires model_id and package")
            model_id = spec["model_id"]
            if type(model_id) is not int or model_id <= 0:
                raise SchemaError(f"compiled {semantic_role} {name} has invalid model_id {model_id!r}")
            if model_id in compiled_model_ids:
                raise SchemaError(f"duplicate compiled model_id {model_id} on {name}")
            compiled_model_ids.add(model_id)
            if "description" in spec and type(spec["description"]) != str:
                raise SchemaError(f"description must be a string on compiled {semantic_role} {name}")
            if "type" in spec and "fields" in spec:
                raise SchemaError(f"compiled {semantic_role} {name} may declare type or fields, not both")
            if "type" in spec and semantic_role != "representation":
                raise SchemaError(f"compiled Type {name} may not declare model-level type")
            value_type = None
            if "type" in spec:
                type_text = spec["type"]
                if type(type_text) != str or not type_text.strip():
                    raise SchemaError(f"compiled representation {name} has invalid type")
                value_type = TypeParser(type_text.strip()).parse()
            fields = spec.get("fields") or {}
            if type(fields) != dict:
                raise SchemaError(f"fields must be a mapping on compiled {semantic_role} {name}")
            module_for(spec["package"]).models.append(
                ModelDef(
                    name=name,
                    description=spec.get("description"),
                    semantic_role=semantic_role,
                    parent=None,
                    value_type=value_type,
                    fields=[parse_field(field_name, field_spec) for field_name, field_spec in fields.items()],
                    variants=[],
                    has_variants=False,
                    model_id=model_id,
                )
            )

    maps = data.get("maps") or {}
    if type(maps) != dict:
        raise SchemaError(f"maps must be a mapping in {path}")
    for name, spec in maps.items():
        if type(spec) != dict:
            raise SchemaError(f"compiled map {name} must be a mapping in {path}")
        unknown = sorted(set(spec) - COMPILED_MAP_KEYS)
        if unknown:
            raise SchemaError(f"unknown keys {unknown} on compiled map {name}")
        if "package" not in spec or "type" not in spec or "value" not in spec:
            raise SchemaError(f"compiled map {name} requires package, type, and value")
        module_for(spec["package"]).maps.append(
            parse_mapping(name, {"type": spec["type"], "value": spec["value"]})
        )

    return list(modules.values())

def load_schema_documents(schema_dir: Path) -> list[ModuleDef]:
    modules: list[ModuleDef] = []
    schema_names: set[str] = set()
    for path in sorted(schema_dir.rglob("*.schema.yaml")):
        relative_parts = path.relative_to(schema_dir).parts
        if len(relative_parts) > CORE_SCHEMA_MAX_PARTS:
            raise SchemaError(f"core schema files are nested too deeply: {path}")
        module, data = parse_document(path)
        if module.doc_type != "schema":
            raise SchemaError(f"type must be schema in core schema dir: {path}")
        if data["package"] in schema_names:
            raise SchemaError(f"duplicate schema package {data['package']} in {path}")
        schema_names.add(data["package"])
        modules.append(module)
    return modules


def load_available_module_documents(module_dir: Path) -> list[ModuleDef]:
    if not module_dir.exists():
        return []
    modules: list[ModuleDef] = []
    for path in sorted(module_dir.rglob("*.schema.yaml")):
        module, data = parse_document(path)
        if module.doc_type != "module":
            raise SchemaError(f"type must be module in module dir: {path}")
        modules.append(module)
    return modules


def select_module_documents(
    available_modules: list[ModuleDef], selected_names: list[str], selected_tags: list[str], all_modules: bool
) -> list[ModuleDef]:
    selected: dict[str, ModuleDef] = {}
    modules_by_name = {module.name: module for module in available_modules}
    if len(modules_by_name) != len(available_modules):
        raise SchemaError("duplicate module packages in module dir")

    selected_tag_set = set(selected_tags)
    if all_modules:
        for module in available_modules:
            selected[module.name] = module
    for module in available_modules:
        if module.name in selected_names or selected_tag_set.intersection(module.tags):
            selected[module.name] = module
        if set(selected_names).intersection(module.tags):
            selected[module.name] = module

    changed = True
    while changed:
        changed = False
        satisfied_names = {"core", *selected}
        satisfied_tags = {"core"}
        for module in selected.values():
            satisfied_tags.update(module.tags)
        for module in list(selected.values()):
            for requirement in module.requires:
                if requirement in satisfied_names or requirement in satisfied_tags:
                    continue
                if requirement in modules_by_name:
                    selected[requirement] = modules_by_name[requirement]
                    changed = True
                    continue
                matching_modules = [candidate for candidate in available_modules if requirement in candidate.tags]
                for candidate in matching_modules:
                    if candidate.name not in selected:
                        selected[candidate.name] = candidate
                        changed = True

    satisfied_names = {"core", *selected}
    satisfied_tags = {"core"}
    for module in selected.values():
        satisfied_tags.update(module.tags)
    for module in selected.values():
        for requirement in module.requires:
            if requirement not in satisfied_names and requirement not in satisfied_tags:
                raise SchemaError(f"unsatisfied requirement {requirement} in {module.path}")
    return sorted(selected.values(), key=lambda module: module.name)


def apply_extend_variants(modules: list[ModuleDef]) -> None:
    models_by_name: dict[str, ModelDef] = {}
    model_paths: dict[str, Path] = {}
    for module in modules:
        for model_def in module.models:
            if model_def.name in models_by_name:
                raise SchemaError(f"duplicate model {model_def.name} in {module.path} and {model_paths[model_def.name]}")
            models_by_name[model_def.name] = model_def
            model_paths[model_def.name] = module.path

    for module in modules:
        if module.doc_type != "module":
            continue
        for parent_name, variant_names in module.extend_variants.items():
            if parent_name not in models_by_name:
                raise SchemaError(f"extend_variants references unknown parent {parent_name} in {module.path}")
            parent_model = models_by_name[parent_name]
            parent_model.has_variants = True
            existing_members = {variant_member_name(parent_name, variant_name) for variant_name in parent_model.variants}
            for variant_name in variant_names:
                if variant_name not in models_by_name:
                    raise SchemaError(f"extend_variants references unknown child {variant_name} in {module.path}")
                if models_by_name[variant_name].parent != parent_name:
                    raise SchemaError(f"extend_variants child {variant_name} parent is not {parent_name} in {module.path}")
                member_name = variant_member_name(parent_name, variant_name)
                if member_name in existing_members:
                    raise SchemaError(f"extend_variants member {parent_name}.{member_name} already exists in {module.path}")
                existing_members.add(member_name)
                parent_model.variants.append(variant_name)


def load_modules(
    schema_dir: Path, module_dir: Path, selected_names: list[str], selected_tags: list[str], all_modules: bool
) -> list[ModuleDef]:
    schema_modules = load_schema_documents(schema_dir)
    selected_modules = select_module_documents(load_available_module_documents(module_dir), selected_names, selected_tags, all_modules)
    modules = schema_modules + selected_modules
    apply_extend_variants(modules)
    return modules


def build_symbol_index(modules: list[ModuleDef]) -> dict[str, str]:
    symbols = {"OCCIDModel": "common", "OCCIDValue": "common", "IntEnum": "common"}
    for module in modules:
        for enum_def in module.enums:
            if enum_def.name in symbols:
                raise SchemaError(f"duplicate symbol {enum_def.name} in {module.path}")
            symbols[enum_def.name] = module.name
        for model_def in module.models:
            if model_def.variants:
                enum_name = variant_enum_name(model_def.name)
                if enum_name in symbols:
                    raise SchemaError(f"duplicate symbol {enum_name} in {module.path}")
                symbols[enum_name] = module.name
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
        for model_def in module.models:
            if model_def.variants:
                enum_name = variant_enum_name(model_def.name)
                members = set(variant_member_name(model_def.name, variant_name) for variant_name in model_def.variants)
                if len(members) != len(model_def.variants):
                    raise SchemaError(f"duplicate derived variant member in {module.path}:{model_def.name}")
                enum_members[enum_name] = members
    return enum_members


def variant_enum_name(model_name: str) -> str:
    return f"{model_name}_type"


def screaming_snake(name: str) -> str:
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


def variant_member_name(parent_name: str, child_name: str) -> str:
    parent_root = parent_name[4:] if parent_name.startswith("Base") else parent_name
    child_root = child_name[4:] if child_name.startswith("Base") else child_name
    if child_root.startswith(parent_root) and child_root != parent_root:
        child_root = child_root[len(parent_root) :]
    elif child_root.endswith(parent_root) and child_root != parent_root:
        child_root = child_root[: -len(parent_root)]
    return screaming_snake(child_root)


def collect_type_refs(node: TypeNode) -> set[str]:
    if node.kind == "fixed_bytes":
        return set()
    if node.kind in {"name", "semantic"}:
        if node.name in PRIMITIVE_TYPES or node.name in TYPE_KEYWORDS:
            return set()
        return {node.name}
    refs: set[str] = set()
    for arg in node.args:
        refs.update(collect_type_refs(arg))
    return refs


def validate_semantic_type_args(
    node: TypeNode,
    *,
    models_by_name: dict[str, ModelDef],
    path: Path,
    location: str,
    authored: bool,
) -> None:
    if node.kind == "semantic":
        if node.name != "IntID":
            raise SchemaError(f"type {node.name} does not take semantic arguments in {path}:{location}")
        if len(node.semantic_args) != 1:
            raise SchemaError(f"IntID requires exactly one namespace in {path}:{location}")
        namespace = node.semantic_args[0]
        if authored and namespace not in models_by_name:
            raise SchemaError(f"unknown IntID namespace {namespace} in {path}:{location}")
        return
    for arg in node.args:
        validate_semantic_type_args(
            arg,
            models_by_name=models_by_name,
            path=path,
            location=location,
            authored=authored,
        )


def validate_schema(modules: list[ModuleDef], symbol_index: dict[str, str], enum_members: dict[str, set[str]]) -> None:
    models_by_name = {model_def.name: model_def for module in modules for model_def in module.models}
    for module in modules:
        if module.doc_type == "schema":
            if module.root not in models_by_name:
                raise SchemaError(f"root {module.root} is not a declared model in {module.path}")
            if models_by_name[module.root].description is None:
                raise SchemaError(f"root model {module.root} is missing description in {module.path}")
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
            if model_def.parent and model_def.parent not in models_by_name:
                raise SchemaError(f"unknown model parent {model_def.parent} in {module.path}")
            if model_def.parent and models_by_name[model_def.parent].value_type is not None:
                raise SchemaError(
                    f"atomic representation {model_def.parent} cannot be a parent in {module.path}:{model_def.name}"
                )
            if model_def.semantic_role == "representation" and not model_def.parent and module.doc_type != "compiled":
                raise SchemaError(f"representation model {model_def.name} must declare a parent in {module.path}")
            if model_def.value_type is not None:
                validate_semantic_type_args(
                    model_def.value_type,
                    models_by_name=models_by_name,
                    path=module.path,
                    location=f"{model_def.name}.type",
                    authored=module.doc_type != "compiled",
                )
                unknown_refs = sorted(ref for ref in collect_type_refs(model_def.value_type) if ref not in symbol_index)
                if unknown_refs:
                    raise SchemaError(f"unknown type refs {unknown_refs} in {module.path}:{model_def.name}.type")
                if model_def.variants:
                    raise SchemaError(f"atomic representation {model_def.name} may not declare variants in {module.path}")
            for variant_name in model_def.variants:
                if variant_name not in symbol_index:
                    raise SchemaError(f"unknown variant {variant_name} in {module.path}:{model_def.name}")
            for field_def in model_def.fields:
                validate_semantic_type_args(
                    field_def.type_node,
                    models_by_name=models_by_name,
                    path=module.path,
                    location=f"{model_def.name}.{field_def.name}",
                    authored=module.doc_type != "compiled",
                )
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
    for module in modules:
        for model_def in module.models:
            for variant_name in model_def.variants:
                if models_by_name[variant_name].parent != model_def.name:
                    raise SchemaError(f"variant {variant_name} parent is not {model_def.name} in {module.path}")


def python_type_expr(node: TypeNode, variant_type_members: dict[str, list[str]]) -> str:
    if node.kind == "fixed_bytes":
        assert node.size is not None
        return f"Annotated[bytes, Field(strict=True, min_length={node.size}, max_length={node.size})]"
    if node.kind == "semantic":
        assert node.name == "IntID"
        assert len(node.semantic_args) == 1
        return f"Annotated[IntID, IDNamespace({node.semantic_args[0]!r})]"
    if node.kind == "name":
        if node.name in PRIMITIVE_TYPES:
            return PRIMITIVE_TYPES[node.name]
        variant_names = variant_type_members.get(node.name) or []
        if variant_names:
            return f"SerializeAsAny[{' | '.join([node.name, *variant_names])}]"
        return node.name
    if node.kind == "list":
        return f"list[{python_type_expr(node.args[0], variant_type_members)}]"
    if node.kind == "map":
        return f"dict[{python_type_expr(node.args[0], variant_type_members)}, {python_type_expr(node.args[1], variant_type_members)}]"
    if node.kind == "tuple":
        return f"tuple[{', '.join(python_type_expr(arg, variant_type_members) for arg in node.args)}]"
    if node.kind == "union":
        return " | ".join(python_type_expr(arg, variant_type_members) for arg in node.args)
    raise SchemaError(f"unsupported type node {node.kind}")


def field_annotation(field_def: FieldDef, variant_type_members: dict[str, list[str]]) -> str:
    python_type = python_type_expr(field_def.type_node, variant_type_members)
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


def field_assignment(field_def: FieldDef, enum_members: dict[str, set[str]], variant_type_members: dict[str, list[str]]) -> str:
    annotation = field_annotation(field_def, variant_type_members)

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
    if any(value.bitflag for value in enum_def.values):
        if has_string_values:
            raise SchemaError(f"bitflag enum {enum_def.name} cannot contain string values")
        return "IntFlag"
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


def render_variant_enum_block(model_def: ModelDef) -> str:
    enum_def = EnumDef(
        name=variant_enum_name(model_def.name),
        values=[
            EnumValue(name=variant_member_name(model_def.name, variant_name), value=0 if index == 0 else None)
            for index, variant_name in enumerate(model_def.variants)
        ],
    )
    return render_enum_block(enum_def)


def model_type_refs(model_def: ModelDef) -> set[str]:
    refs: set[str] = set()
    if model_def.parent:
        refs.add(model_def.parent)
    if model_def.value_type is not None:
        refs.update(collect_type_refs(model_def.value_type))
    for field_def in model_def.fields:
        refs.update(collect_type_refs(field_def.type_node))
    return refs


def runtime_type_refs(model_def: ModelDef, enum_members: dict[str, set[str]]) -> set[str]:
    refs: set[str] = set()
    if model_def.parent:
        refs.add(model_def.parent)
    if model_def.value_type is not None:
        refs.update(collect_type_refs(model_def.value_type))
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


def render_model_block(
    model_def: ModelDef,
    enum_members: dict[str, set[str]],
    variant_type_members: dict[str, list[str]],
) -> str:
    if model_def.value_type is not None:
        parent = f"OCCIDValue[{python_type_expr(model_def.value_type, variant_type_members)}]"
    else:
        parent = model_def.parent or "OCCIDModel"
    lines = [f"class {model_def.name}({parent}):"]
    if model_def.description:
        lines.append(f"    {model_def.description!r}")
    if model_def.model_id is None:
        raise SchemaError(f"runtime model {model_def.name} is missing compiled model_id")
    lines.append(f"    __occid_model_id__: ClassVar[int] = {model_def.model_id}")
    if model_def.semantic_role:
        lines.append(f"    __occid_semantic_role__: ClassVar[str] = {model_def.semantic_role!r}")
    for field_def in model_def.fields:
        lines.append(f"    {field_def.name}: {field_assignment(field_def, enum_members, variant_type_members)}")
    return "\n".join(lines)


def mapping_key_literal(key: object, key_type: str, enum_members: dict[str, set[str]]) -> str:
    if key_type in enum_members:
        return f"{key_type}.{key}"
    return repr(key)


def mapping_value_literal(value: object, value_type: str, enum_members: dict[str, set[str]]) -> str:
    if value_type in enum_members:
        return f"{value_type}.{value}"
    return repr(value)


def render_mapping_block(mapping_def: MappingDef, enum_members: dict[str, set[str]], variant_type_members: dict[str, list[str]]) -> str:
    lines = [
        f"{mapping_def.name}: dict[{python_type_expr(TypeParser(mapping_def.key_type).parse(), variant_type_members)}, {python_type_expr(TypeParser(mapping_def.value_type).parse(), variant_type_members)}] = {{"
    ]
    for key, value in mapping_def.entries.items():
        key_expr = mapping_key_literal(key, mapping_def.key_type, enum_members)
        value_expr = mapping_value_literal(value, mapping_def.value_type, enum_members)
        lines.append(f"    {key_expr}: {value_expr},")
    lines.append("}")
    return "\n".join(lines)


def render_common_runtime() -> str:
    sections = [load_template("common_header.py"), load_template("common_intenum.py"), load_template("common_runtime.py")]
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def render_module(
    module: ModuleDef,
    symbol_index: dict[str, str],
    enum_members: dict[str, set[str]],
    variant_type_members: dict[str, list[str]],
) -> str:
    sections = [load_template("module_header.py")]
    imports = module_imports(module, symbol_index, enum_members)
    if imports:
        sections.append("\n".join(imports))
    if module.enums:
        sections.append("### Enums")
        enum_blocks = [render_enum_block(enum_def) for enum_def in module.enums]
        sections.append("\n\n".join(enum_blocks))
    if module.maps:
        sections.append("### Mappings")
        sections.append(
            "\n\n".join(render_mapping_block(mapping_def, enum_members, variant_type_members) for mapping_def in module.maps)
        )
    if module.models:
        sections.append("### Models")
        sections.append(
            "\n\n".join(render_model_block(model_def, enum_members, variant_type_members) for model_def in module.models)
        )
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def render_common_schema_module(
    module: ModuleDef,
    enum_members: dict[str, set[str]],
    variant_type_members: dict[str, list[str]],
) -> str:
    sections = []
    if module.enums:
        sections.append("### Schema Enums")
        enum_blocks = [render_enum_block(enum_def) for enum_def in module.enums]
        sections.append("\n\n".join(enum_blocks))
    if module.maps:
        sections.append("### Schema Mappings")
        sections.append(
            "\n\n".join(render_mapping_block(mapping_def, enum_members, variant_type_members) for mapping_def in module.maps)
        )
    if module.models:
        sections.append("### Schema Models")
        sections.append(
            "\n\n".join(render_model_block(model_def, enum_members, variant_type_members) for model_def in module.models)
        )
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip()


def build_variant_type_members(modules: list[ModuleDef], symbol_index: dict[str, str]) -> dict[str, list[str]]:
    schema_module_names = {module.name for module in modules if module.doc_type == "schema"}
    models_by_name = {model_def.name: model_def for module in modules for model_def in module.models}
    children_by_parent: dict[str, list[str]] = {}
    for model_def in models_by_name.values():
        if model_def.parent:
            children_by_parent.setdefault(model_def.parent, []).append(model_def.name)
    variant_type_members: dict[str, list[str]] = {}

    def collect_schema_variants(model_name: str, seen: set[str]) -> list[str]:
        variant_names: list[str] = []
        for variant_name in [*models_by_name[model_name].variants, *children_by_parent.get(model_name, [])]:
            if variant_name in seen:
                continue
            seen.add(variant_name)
            if symbol_index[variant_name] not in schema_module_names:
                continue
            variant_names.append(variant_name)
            variant_names.extend(collect_schema_variants(variant_name, seen))
        return variant_names

    for module in modules:
        for model_def in module.models:
            variant_names = collect_schema_variants(model_def.name, set())
            if variant_names:
                variant_type_members[model_def.name] = variant_names
    return variant_type_members


def module_dependency_graph(
    modules: list[ModuleDef], symbol_index: dict[str, str], enum_members: dict[str, set[str]]
) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    module_names = {module.name for module in modules}
    for module in modules:
        refs: set[str] = set()
        for requirement in module.requires:
            if requirement in module_names and requirement != module.name:
                refs.add(requirement)
        for mapping_def in module.maps:
            for ref in (mapping_def.key_type, mapping_def.value_type):
                if ref in symbol_index and symbol_index[ref] != module.name:
                    refs.add(symbol_index[ref])
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
    lines.extend(f"from .{name} import *" for name in module_names if name != "common")
    lines.extend(
        [
            "",
            "for _model in [obj for obj in list(globals().values()) if (OCCIDModel in getattr(obj, \"__mro__\", ()) or OCCIDValue in getattr(obj, \"__mro__\", ())) and obj not in {OCCIDModel, OCCIDValue}]:",
            "    _model.model_rebuild(_types_namespace=globals())",
        ]
    )
    lines.append("")
    lines.append('__all__ = [name for name in globals() if not name.startswith("_")]')
    return "\n".join(lines) + "\n"


def write_package(
    output_dir: Path,
    modules: list[ModuleDef],
    symbol_index: dict[str, str],
    enum_members: dict[str, set[str]],
) -> None:
    graph = module_dependency_graph(modules, symbol_index, enum_members)
    ordered_names = topo_sort_modules(modules, graph)
    module_map = {module.name: module for module in modules}
    variant_type_members = build_variant_type_members(modules, symbol_index)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    common_sections = [render_common_runtime().rstrip()]
    if "common" in module_map:
        common_sections.append(render_common_schema_module(module_map["common"], enum_members, variant_type_members))
    (output_dir / "common.py").write_text("\n\n".join(section for section in common_sections if section).rstrip() + "\n")

    for module_name in ordered_names:
        if module_name == "common":
            continue
        module = module_map[module_name]
        (output_dir / f"{module_name}.py").write_text(
            render_module(module, symbol_index, enum_members, variant_type_members)
        )

    (output_dir / "__init__.py").write_text(render_init(ordered_names))


def main() -> None:
    args = parse_args()
    modules = load_compiled_schema(args.input)
    symbol_index = build_symbol_index(modules)
    enum_members = build_enum_members(modules)
    validate_schema(modules, symbol_index, enum_members)
    write_package(args.output_dir, modules, symbol_index, enum_members)
    print(f"input={args.input}")
    print(f"output_dir={args.output_dir}")
    print(f"module_count={len(modules)}")


if __name__ == "__main__":
    main()
