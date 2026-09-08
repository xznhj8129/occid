#!/usr/bin/env python3
"""Generate the OCCID TypeScript binding from the compiled ``occid.yaml``.

The TypeScript binding is a sibling of the generated Pydantic binding.  It is
not generated from OpenAPI and does not depend on Sigma.

Generated runtime features:
  * every OCCID model and vocabulary as TypeScript types/values;
  * semantic model unions derived from the OCCID parent graph;
  * model/enum registries and ``isA`` / ``childrenOf``;
  * runtime validation and model construction with Pydantic-like defaults;
  * lossless named JSON ``toData`` / ``fromData`` and ``dumps`` / ``loads``;
  * compact wire envelope ``toWireEnvelope`` / ``fromWireEnvelope``;
  * UID/bytes, large integer, tuple, map, enum and IntFlag handling;
  * schema maps and OCCID contract/version metadata.

The compact helpers intentionally stop at the structural MessagePack envelope.
They do not embed a JavaScript MessagePack implementation. Browser HTTP use needs
the named JSON codec; binary transports can pass the envelope to their chosen
MessagePack implementation without duplicating OCCID semantics.

The generated materialized model representation is deliberately simple:

    { $model: "TaskManeuver", ...fields }

Atomic OCCIDValue representations are:

    { $model: "UID", value: Uint8Array(...) }

``toData`` converts those materialized values to OCCID's named JSON envelope:

    { model: "TaskManeuver", value: { ... } }

No handwritten OCCID model list exists in this generator.  All model sets,
field shapes, enum values and ancestry come from the compiled schema.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import generate_pydantic as idl


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = REPO_ROOT / "occid.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "typescript" / "occid.ts"
DEFAULT_VERSION = REPO_ROOT / "VERSION"
DEFAULT_CONTRACT = REPO_ROOT / "occid-contract.json"

TS_PRIMITIVES = {
    "string": "string",
    "int": "OCCIDInteger",
    "int8": "OCCIDInteger",
    "int16": "OCCIDInteger",
    "int32": "OCCIDInteger",
    "int64": "OCCIDInteger",
    "uint8": "OCCIDInteger",
    "uint16": "OCCIDInteger",
    "uint32": "OCCIDInteger",
    "uint64": "OCCIDInteger",
    "float": "number",
    "bool": "boolean",
    "bytes": "Uint8Array",
    "any": "unknown",
}
INTEGER_PRIMITIVES = {
    "int", "int8", "int16", "int32", "int64",
    "uint8", "uint16", "uint32", "uint64",
}


class GenerationError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--version-file", type=Path, default=DEFAULT_VERSION)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    return parser.parse_args()


def q(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def resolved_enum_values(enum_def: idl.EnumDef) -> list[tuple[str, int | str]]:
    result: list[tuple[str, int | str]] = []
    next_value: int | None = None
    for index, entry in enumerate(enum_def.values):
        if isinstance(entry.value, str):
            result.append((entry.name, entry.value))
            next_value = None
            continue
        if isinstance(entry.value, int):
            result.append((entry.name, entry.value))
            next_value = entry.value + 1
            continue
        if index == 0 or next_value is None:
            raise GenerationError(
                f"first enum member {enum_def.name}.{entry.name} must have an explicit value"
            )
        result.append((entry.name, next_value))
        next_value += 1
    return result


def is_flag_enum(enum_def: idl.EnumDef) -> bool:
    return any(value.bitflag for value in enum_def.values)


def descendants(models: dict[str, idl.ModelDef], name: str) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    def visit(current: str) -> None:
        for child in models[current].children:
            if child in seen:
                continue
            if child not in models:
                raise GenerationError(f"unknown child {child!r} of {current!r}")
            seen.add(child)
            result.append(child)
            visit(child)

    visit(name)
    return result


def type_spec_expr(
    node: idl.TypeNode,
    model_names: set[str],
    enum_names: set[str],
) -> str:
    if node.kind == "fixed_bytes":
        assert node.size is not None
        return f'{{kind:"fixedBytes",size:{node.size}}}'
    if node.kind == "semantic":
        if node.name != "IntID" or len(node.semantic_args) != 1:
            raise GenerationError(f"unsupported semantic type {node}")
        return f'{{kind:"namespacedIntID",namespace:{q(node.semantic_args[0])}}}'
    if node.kind == "name":
        assert node.name is not None
        if node.name in TS_PRIMITIVES:
            return f'{{kind:"primitive",name:{q(node.name)}}}'
        if node.name in model_names:
            return f'{{kind:"model",name:{q(node.name)}}}'
        if node.name in enum_names:
            return f'{{kind:"enum",name:{q(node.name)}}}'
        raise GenerationError(f"unknown type name {node.name!r}")
    if node.kind == "list":
        return f'{{kind:"list",item:{type_spec_expr(node.args[0], model_names, enum_names)}}}'
    if node.kind == "map":
        return (
            '{kind:"map",key:'
            + type_spec_expr(node.args[0], model_names, enum_names)
            + ',value:'
            + type_spec_expr(node.args[1], model_names, enum_names)
            + '}'
        )
    if node.kind == "tuple":
        return '{kind:"tuple",items:[' + ",".join(
            type_spec_expr(arg, model_names, enum_names) for arg in node.args
        ) + ']}'
    if node.kind == "union":
        return '{kind:"union",items:[' + ",".join(
            type_spec_expr(arg, model_names, enum_names) for arg in node.args
        ) + ']}'
    raise GenerationError(f"unsupported type node kind {node.kind!r}")


def ts_type(
    node: idl.TypeNode,
    model_names: set[str],
    enum_names: set[str],
) -> str:
    if node.kind == "fixed_bytes":
        return "Uint8Array"
    if node.kind == "semantic":
        if node.name != "IntID" or len(node.semantic_args) != 1:
            raise GenerationError(f"unsupported semantic type {node}")
        return f'NamespacedIntID<{q(node.semantic_args[0])}>'
    if node.kind == "name":
        assert node.name is not None
        if node.name in TS_PRIMITIVES:
            return TS_PRIMITIVES[node.name]
        if node.name in model_names or node.name in enum_names:
            return node.name
        raise GenerationError(f"unknown type name {node.name!r}")
    if node.kind == "list":
        return f"Array<{ts_type(node.args[0], model_names, enum_names)}>"
    if node.kind == "map":
        return (
            f"Map<{ts_type(node.args[0], model_names, enum_names)}, "
            f"{ts_type(node.args[1], model_names, enum_names)}>"
        )
    if node.kind == "tuple":
        return "[" + ", ".join(ts_type(arg, model_names, enum_names) for arg in node.args) + "]"
    if node.kind == "union":
        return "(" + " | ".join(ts_type(arg, model_names, enum_names) for arg in node.args) + ")"
    raise GenerationError(f"unsupported type node kind {node.kind!r}")


def field_ts_type(
    field: idl.FieldDef,
    model_names: set[str],
    enum_names: set[str],
) -> str:
    value = ts_type(field.type_node, model_names, enum_names)
    return f"{value} | null" if field.optional else value


def default_spec(field: idl.FieldDef, enum_names: set[str]) -> str:
    if field.optional and not field.has_default:
        return '{kind:"literal",value:null}'
    if not field.has_default:
        return "null"
    if field.default is None:
        return '{kind:"literal",value:null}'
    if (
        field.type_node.kind == "name"
        and field.type_node.name in enum_names
        and isinstance(field.default, str)
    ):
        return (
            '{kind:"enum",enum:' + q(field.type_node.name)
            + ',member:' + q(field.default) + '}'
        )
    # Compiled OCCID currently uses only JSON-safe scalar explicit defaults.
    # Keep this generic so future list/map/object defaults remain representable.
    return '{kind:"literal",value:' + q(field.default) + '}'


def render_runtime_header(version: str, contract_hash: str | None) -> str:
    contract_line = (
        f"export const OCCID_CONTRACT_GLOBAL_HASH = {q(contract_hash)} as const;"
        if contract_hash
        else "export const OCCID_CONTRACT_GLOBAL_HASH: string | null = null;"
    )
    return f'''// GENERATED by generate_typescript.py. Do not edit.
// Source: compiled OCCID runtime schema (occid.yaml).

export const OCCID_VERSION = {q(version)} as const;
{contract_line}
export const SAFE_INTEGER = 9007199254740991;

export type OCCIDInteger = number | bigint;
type StringMap<T = unknown> = {{ [key: string]: T }};
export type SemanticRole = "concept" | "representation";
export type PrimitiveName =
  | "string" | "int" | "int8" | "int16" | "int32" | "int64"
  | "uint8" | "uint16" | "uint32" | "uint64"
  | "float" | "bool" | "bytes" | "any";

export interface OCCIDModelValue<N extends string = string> {{ readonly $model: N }}
export interface OCCIDAtomicValue<N extends string = string, V = unknown> {{
  readonly $model: N;
  value: V;
}}
export interface OCCIDEnumValue<E extends string = string, N extends string = string, V extends number | string = number | string> {{
  readonly $enum: E;
  readonly name: N;
  readonly value: V;
  readonly $flags?: false;
}}
export interface OCCIDFlagValue<E extends string = string> {{
  readonly $enum: E;
  readonly names: readonly string[];
  readonly value: number;
  readonly $flags: true;
}}
export type NamespacedIntID<N extends string> = IntID & {{ readonly __idNamespace?: N }};

export type TypeSpec =
  | {{ readonly kind: "primitive"; readonly name: PrimitiveName }}
  | {{ readonly kind: "fixedBytes"; readonly size: number }}
  | {{ readonly kind: "model"; readonly name: ModelName }}
  | {{ readonly kind: "enum"; readonly name: EnumName }}
  | {{ readonly kind: "namespacedIntID"; readonly namespace: string }}
  | {{ readonly kind: "list"; readonly item: TypeSpec }}
  | {{ readonly kind: "map"; readonly key: TypeSpec; readonly value: TypeSpec }}
  | {{ readonly kind: "tuple"; readonly items: readonly TypeSpec[] }}
  | {{ readonly kind: "union"; readonly items: readonly TypeSpec[] }};

export type DefaultSpec =
  | {{ readonly kind: "literal"; readonly value: unknown }}
  | {{ readonly kind: "enum"; readonly enum: EnumName; readonly member: string }};

export interface FieldSpec {{
  readonly type: TypeSpec;
  readonly optional: boolean;
  readonly const: boolean;
  readonly default: DefaultSpec | null;
}}
export interface ModelSpec {{
  readonly id: number;
  readonly package: string;
  readonly semanticRole: SemanticRole;
  readonly parent: ModelName | null;
  readonly children: readonly ModelName[];
  readonly atomic: boolean;
  readonly valueType?: TypeSpec;
  readonly fields: Readonly<StringMap<FieldSpec>>;
  readonly fieldOrder: readonly string[];
}}
export interface EnumSpec {{
  readonly package: string;
  readonly flags: boolean;
  readonly members: Readonly<StringMap<number | string>>;
}}

const PRESENT_FIELDS = Symbol("occid.presentFields");
const TUPLE_VALUE = Symbol("occid.tuple");
const RESERVED_TAGS = new Set(["model", "enum", "$bytes", "$integer", "$map", "$tuple", "$text"]);

export class CodecError extends Error {{
  constructor(message: string) {{ super(message); this.name = "CodecError"; }}
}}

function hasOwn(value: object, key: PropertyKey): boolean {{
  return Object.prototype.hasOwnProperty.call(value, key);
}}

function isPlainObject(value: unknown): value is StringMap<unknown> {{
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}}

function exactKeys(value: StringMap<unknown>, expected: readonly string[]): boolean {{
  const keys = Object.keys(value);
  return keys.length === expected.length && expected.every((key) => hasOwn(value, key));
}}

function isSafeIntegerNumber(value: unknown): value is number {{
  return typeof value === "number" && Number.isSafeInteger(value);
}}

function integerValue(value: unknown, path: string): OCCIDInteger {{
  if (typeof value === "bigint") return value;
  if (isSafeIntegerNumber(value)) return value;
  throw new CodecError(`${{path}} requires an integer`);
}}

function finiteNumber(value: unknown, path: string): number {{
  if (typeof value !== "number" || !Number.isFinite(value))
    throw new CodecError(`${{path}} requires a finite number`);
  return value;
}}

function hexToBytes(value: unknown, path: string): Uint8Array {{
  if (typeof value !== "string" || !/^(?:[0-9a-f]{{2}})*$/.test(value))
    throw new CodecError(`${{path}} requires an even number of lowercase hexadecimal digits`);
  const out = new Uint8Array(value.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = Number.parseInt(value.slice(i * 2, i * 2 + 2), 16);
  return out;
}}

function bytesToHex(value: Uint8Array): string {{
  let out = "";
  for (const byte of value) out += byte.toString(16).padStart(2, "0");
  return out;
}}

function encodeUtf8SurrogatePass(value: string): Uint8Array {{
  const out: number[] = [];
  for (let i = 0; i < value.length; i++) {{
    let cp = value.charCodeAt(i);
    if (cp >= 0xd800 && cp <= 0xdbff && i + 1 < value.length) {{
      const lo = value.charCodeAt(i + 1);
      if (lo >= 0xdc00 && lo <= 0xdfff) {{
        cp = 0x10000 + ((cp - 0xd800) << 10) + (lo - 0xdc00);
        i++;
      }}
    }}
    if (cp <= 0x7f) out.push(cp);
    else if (cp <= 0x7ff) out.push(0xc0 | (cp >> 6), 0x80 | (cp & 0x3f));
    else if (cp <= 0xffff) out.push(0xe0 | (cp >> 12), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f));
    else out.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3f), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f));
  }}
  return Uint8Array.from(out);
}}

function decodeUtf8SurrogatePass(bytes: Uint8Array, path: string): string {{
  let out = "";
  for (let i = 0; i < bytes.length;) {{
    const b0 = bytes[i++];
    let cp: number;
    if (b0 <= 0x7f) cp = b0;
    else if ((b0 & 0xe0) === 0xc0) {{
      if (i >= bytes.length) throw new CodecError(`${{path}} contains truncated UTF-8`);
      const b1 = bytes[i++]; if ((b1 & 0xc0) !== 0x80) throw new CodecError(`${{path}} contains invalid UTF-8`);
      cp = ((b0 & 0x1f) << 6) | (b1 & 0x3f); if (cp < 0x80) throw new CodecError(`${{path}} contains overlong UTF-8`);
    }} else if ((b0 & 0xf0) === 0xe0) {{
      if (i + 1 >= bytes.length) throw new CodecError(`${{path}} contains truncated UTF-8`);
      const b1 = bytes[i++], b2 = bytes[i++];
      if ((b1 & 0xc0) !== 0x80 || (b2 & 0xc0) !== 0x80) throw new CodecError(`${{path}} contains invalid UTF-8`);
      cp = ((b0 & 0x0f) << 12) | ((b1 & 0x3f) << 6) | (b2 & 0x3f);
      if (cp < 0x800) throw new CodecError(`${{path}} contains overlong UTF-8`);
    }} else if ((b0 & 0xf8) === 0xf0) {{
      if (i + 2 >= bytes.length) throw new CodecError(`${{path}} contains truncated UTF-8`);
      const b1 = bytes[i++], b2 = bytes[i++], b3 = bytes[i++];
      if ((b1 & 0xc0) !== 0x80 || (b2 & 0xc0) !== 0x80 || (b3 & 0xc0) !== 0x80)
        throw new CodecError(`${{path}} contains invalid UTF-8`);
      cp = ((b0 & 7) << 18) | ((b1 & 0x3f) << 12) | ((b2 & 0x3f) << 6) | (b3 & 0x3f);
      if (cp < 0x10000 || cp > 0x10ffff) throw new CodecError(`${{path}} contains invalid UTF-8 code point`);
    }} else throw new CodecError(`${{path}} contains invalid UTF-8`);

    if (cp <= 0xffff) out += String.fromCharCode(cp);
    else {{ cp -= 0x10000; out += String.fromCharCode(0xd800 + (cp >> 10), 0xdc00 + (cp & 0x3ff)); }}
  }}
  return out;
}}

function containsUnsafeJsonText(value: string): boolean {{
  if (value.includes("\\0")) return true;
  for (let i = 0; i < value.length; i++) {{
    const c = value.charCodeAt(i);
    if (c >= 0xd800 && c <= 0xdbff) {{
      const next = value.charCodeAt(i + 1);
      if (next >= 0xdc00 && next <= 0xdfff) i++;
      else return true;
    }} else if (c >= 0xdc00 && c <= 0xdfff) return true;
  }}
  return false;
}}

export function tuple<T extends readonly unknown[]>(...items: T): T {{
  const value = items as unknown as T & {{ [TUPLE_VALUE]?: true }};
  Object.defineProperty(value, TUPLE_VALUE, {{ value: true, enumerable: false }});
  return value;
}}

function isTupleValue(value: unknown): boolean {{
  return Array.isArray(value) && (value as unknown as {{ [TUPLE_VALUE]?: boolean }})[TUPLE_VALUE] === true;
}}

function enumValue<E extends string, N extends string, V extends number | string>(
  enumName: E, name: N, value: V,
): OCCIDEnumValue<E, N, V> {{
  return Object.freeze({{ $enum: enumName, name, value, $flags: false as const }});
}}

function flagValue<E extends string>(enumName: E, names: readonly string[], value: number): OCCIDFlagValue<E> {{
  return Object.freeze({{ $enum: enumName, names: Object.freeze([...names]), value, $flags: true as const }});
}}
'''


def render_enums(modules: list[idl.ModuleDef]) -> str:
    blocks: list[str] = ["// OCCID vocabularies"]
    enum_defs = sorted((e for m in modules for e in m.enums), key=lambda e: e.name)
    for enum_def in enum_defs:
        values = resolved_enum_values(enum_def)
        if is_flag_enum(enum_def):
            members = "\n".join(
                f"  {name}: flagValue({q(enum_def.name)}, [{q(name)}], {value}),"
                for name, value in values
            )
            blocks.append(
                f"export const {enum_def.name} = Object.freeze({{\n{members}\n}});\n"
                f"export type {enum_def.name} = OCCIDFlagValue<{q(enum_def.name)}>;"
            )
        else:
            members = "\n".join(
                f"  {name}: enumValue({q(enum_def.name)}, {q(name)}, {q(value)}),"
                for name, value in values
            )
            blocks.append(
                f"export const {enum_def.name} = Object.freeze({{\n{members}\n}});\n"
                f"export type {enum_def.name} = (typeof {enum_def.name})[keyof typeof {enum_def.name}];"
            )
    names = " | ".join(q(e.name) for e in enum_defs) or "never"
    blocks.insert(1, f"export type EnumName = {names};")
    return "\n\n".join(blocks)


def render_models(modules: list[idl.ModuleDef]) -> str:
    models = {m.name: m for module in modules for m in module.models}
    model_names = set(models)
    enum_names = {e.name for module in modules for e in module.enums}
    lines: list[str] = ["// OCCID materialized model types"]

    for name in sorted(models):
        model = models[name]
        if model.value_type is not None:
            value_type = ts_type(model.value_type, model_names, enum_names)
            lines.append(
                f"export interface {name}$Exact extends OCCIDAtomicValue<{q(name)}, {value_type}> {{}}"
            )
            lines.append(f"export type {name}$Input = {value_type};")
            continue

        fields = []
        input_fields = []
        for field in model.fields:
            t = field_ts_type(field, model_names, enum_names)
            fields.append(f"  {field.name}: {t};")
            optional_input = field.optional or field.has_default
            marker = "?" if optional_input else ""
            input_fields.append(f"  {field.name}{marker}: {t};")
        body = "\n".join(fields)
        input_body = "\n".join(input_fields)
        lines.append(
            f"export interface {name}$Exact extends OCCIDModelValue<{q(name)}> {{\n{body}\n}}"
        )
        lines.append(f"export interface {name}$Input {{\n{input_body}\n}}")

    lines.append("// Semantic aliases include each model and all descendants in the compiled parent graph.")
    for name in sorted(models):
        union = [name, *descendants(models, name)]
        union_text = " | ".join(f"{item}$Exact" for item in union)
        lines.append(f"export type {name} = {union_text};")

    names = " | ".join(q(name) for name in sorted(models)) or "never"
    lines.append(f"export type ModelName = {names};")
    lines.append("export type OCCIDValue = " + " | ".join(f"{n}$Exact" for n in sorted(models)) + ";")

    lines.append("export interface ExactModelMap {")
    for name in sorted(models):
        lines.append(f"  {name}: {name}$Exact;")
    lines.append("}")
    lines.append("export interface SemanticModelMap {")
    for name in sorted(models):
        lines.append(f"  {name}: {name};")
    lines.append("}")
    lines.append("export interface ModelInputMap {")
    for name in sorted(models):
        lines.append(f"  {name}: {name}$Input;")
    lines.append("}")
    return "\n\n".join(lines)


def render_enum_registry(modules: list[idl.ModuleDef]) -> str:
    entries = []
    for module in modules:
        for enum_def in module.enums:
            values = resolved_enum_values(enum_def)
            members = "{" + ",".join(f"{q(name)}:{q(value)}" for name, value in values) + "}"
            entries.append(
                f"  {q(enum_def.name)}: {{package:{q(module.name)},flags:{str(is_flag_enum(enum_def)).lower()},members:{members}}},"
            )
    return "export const ENUM_REGISTRY: Readonly<StringMap<EnumSpec>> = Object.freeze({\n" + "\n".join(sorted(entries)) + "\n});"


def render_model_registry(modules: list[idl.ModuleDef]) -> str:
    model_names = {m.name for module in modules for m in module.models}
    enum_names = {e.name for module in modules for e in module.enums}
    entries: list[str] = []
    for module in modules:
        for model in module.models:
            if model.model_id is None:
                raise GenerationError(f"model {model.name} has no compiled model ID")
            field_entries = []
            for field in model.fields:
                field_entries.append(
                    f"{q(field.name)}:{{type:{type_spec_expr(field.type_node, model_names, enum_names)},"
                    f"optional:{str(field.optional).lower()},const:{str(field.const).lower()},"
                    f"default:{default_spec(field, enum_names)}}}"
                )
            fields = "{" + ",".join(field_entries) + "}"
            order = q([field.name for field in model.fields])
            value_type = (
                f",valueType:{type_spec_expr(model.value_type, model_names, enum_names)}"
                if model.value_type is not None else ""
            )
            entries.append(
                f"  {q(model.name)}: {{id:{model.model_id},package:{q(module.name)},"
                f"semanticRole:{q(model.semantic_role)},parent:{q(model.parent)},children:{q(model.children)},"
                f"atomic:{str(model.value_type is not None).lower()}{value_type},fields:{fields},fieldOrder:{order}}},"
            )
    by_id = sorted(
        (model.model_id, model.name)
        for module in modules for model in module.models
        if model.model_id is not None
    )
    return (
        "export const MODEL_REGISTRY: Readonly<StringMap<ModelSpec>> = Object.freeze({\n"
        + "\n".join(sorted(entries))
        + "\n});\n\n"
        + "export const MODEL_NAME_BY_ID: Readonly<{ readonly [key: number]: ModelName }> = Object.freeze({\n"
        + "\n".join(f"  {model_id}: {q(name)}," for model_id, name in by_id)
        + "\n});"
    )


def render_runtime_body() -> str:
    return r'''
export function isA(actual: OCCIDValue | ModelName, expected: ModelName): boolean {
  let current: ModelName | null = typeof actual === "string" ? actual : actual.$model;
  const seen = new globalThis.Set<ModelName>();
  while (current !== null) {
    if (current === expected) return true;
    if (seen.has(current)) throw new Error(`OCCID semantic parent cycle involving ${current}`);
    seen.add(current);
    current = MODEL_REGISTRY[current].parent;
  }
  return false;
}

export function childrenOf(model: OCCIDValue | ModelName): readonly ModelName[] {
  const name = typeof model === "string" ? model : model.$model;
  return MODEL_REGISTRY[name].children;
}

export function modelFieldsSet(value: OCCIDValue): ReadonlySet<string> {
  const spec = MODEL_REGISTRY[value.$model];
  if (spec.atomic) return new globalThis.Set(["value"]);
  const present = (value as unknown as { [PRESENT_FIELDS]?: globalThis.Set<string> })[PRESENT_FIELDS];
  return new globalThis.Set(present ?? spec.fieldOrder.filter((name) => hasOwn(value as object, name)));
}

function enumMemberByName(enumName: EnumName, member: string): OCCIDEnumValue | OCCIDFlagValue {
  const spec = ENUM_REGISTRY[enumName];
  if (!hasOwn(spec.members, member)) throw new CodecError(`unknown ${enumName} member ${member}`);
  const raw = spec.members[member];
  if (spec.flags) {
    if (typeof raw !== "number") throw new CodecError(`flag enum ${enumName}.${member} is not numeric`);
    return flagValue(enumName, [member], raw);
  }
  return enumValue(enumName, member, raw);
}

export function makeFlags<E extends EnumName>(enumName: E, ...names: string[]): OCCIDFlagValue<E> {
  const spec = ENUM_REGISTRY[enumName];
  if (!spec.flags) throw new CodecError(`${enumName} is not a flag vocabulary`);
  let value = 0;
  const unique: string[] = [];
  for (const name of names) {
    if (!hasOwn(spec.members, name)) throw new CodecError(`unknown ${enumName} flag ${name}`);
    const raw = spec.members[name];
    if (typeof raw !== "number") throw new CodecError(`flag enum ${enumName}.${name} is not numeric`);
    if (!unique.includes(name)) unique.push(name);
    value |= raw;
  }
  return flagValue(enumName, unique, value);
}

function cloneDefault(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(cloneDefault);
  if (isPlainObject(value)) {
    const out: StringMap<unknown> = {};
    for (const [key, item] of Object.entries(value)) out[key] = cloneDefault(item);
    return out;
  }
  return value;
}

function materializeDefault(spec: DefaultSpec): unknown {
  if (spec.kind === "enum") return enumMemberByName(spec.enum, spec.member);
  return cloneDefault(spec.value);
}

function validatePrimitive(name: PrimitiveName, value: unknown, path: string): unknown {
  switch (name) {
    case "string":
      if (typeof value !== "string") throw new CodecError(`${path} requires a string`);
      return value;
    case "bool":
      if (typeof value !== "boolean") throw new CodecError(`${path} requires a boolean`);
      return value;
    case "float":
      return finiteNumber(value, path);
    case "int": case "int8": case "int16": case "int32": case "int64":
    case "uint8": case "uint16": case "uint32": case "uint64":
      return integerValue(value, path);
    case "bytes":
      if (!(value instanceof Uint8Array)) throw new CodecError(`${path} requires Uint8Array`);
      return value;
    case "any":
      return value;
  }
}

function validateMaterialized(spec: TypeSpec, value: unknown, path: string): unknown {
  switch (spec.kind) {
    case "primitive": return validatePrimitive(spec.name, value, path);
    case "fixedBytes":
      if (!(value instanceof Uint8Array) || value.length !== spec.size)
        throw new CodecError(`${path} requires exactly ${spec.size} bytes`);
      return value;
    case "model":
      if (!isOccidValue(value) || !isA(value, spec.name))
        throw new CodecError(`${path} requires semantic ${spec.name}`);
      return value;
    case "namespacedIntID":
      if (!isOccidValue(value) || !isA(value, "IntID"))
        throw new CodecError(`${path} requires IntID(${spec.namespace})`);
      return value;
    case "enum":
      if (!isEnumValue(value) || value.$enum !== spec.name)
        throw new CodecError(`${path} requires enum ${spec.name}`);
      return value;
    case "list":
      if (!Array.isArray(value) || isTupleValue(value)) throw new CodecError(`${path} requires a list`);
      return value.map((item, index) => validateMaterialized(spec.item, item, `${path}[${index}]`));
    case "map": {
      if (!(value instanceof Map)) throw new CodecError(`${path} requires Map`);
      const out = new Map<unknown, unknown>();
      let index = 0;
      for (const [key, item] of value) {
        out.set(
          validateMaterialized(spec.key, key, `${path}.key[${index}]`),
          validateMaterialized(spec.value, item, `${path}.value[${index}]`),
        );
        index++;
      }
      return out;
    }
    case "tuple":
      if (!Array.isArray(value) || value.length !== spec.items.length)
        throw new CodecError(`${path} requires a ${spec.items.length}-item tuple`);
      return tuple(...spec.items.map((itemSpec, index) => validateMaterialized(itemSpec, value[index], `${path}[${index}]`)));
    case "union": {
      let last: unknown = null;
      for (const item of spec.items) {
        try { return validateMaterialized(item, value, path); }
        catch (error) { last = error; }
      }
      throw last instanceof Error ? last : new CodecError(`${path} does not satisfy any union member`);
    }
  }
}

function makeRecordModel(name: ModelName, rawFields: StringMap<unknown>, path: string): OCCIDValue {
  const spec = MODEL_REGISTRY[name];
  if (spec.atomic) throw new CodecError(`${name} is atomic`);
  const allowed = new Set(spec.fieldOrder);
  for (const key of Object.keys(rawFields)) {
    if (!allowed.has(key)) throw new CodecError(`${path}.${key} is not a field of ${name}`);
  }

  const target: { [key: PropertyKey]: unknown } = { $model: name };
  const present = new globalThis.Set<string>();
  for (const fieldName of spec.fieldOrder) {
    const field = spec.fields[fieldName];
    if (hasOwn(rawFields, fieldName)) {
      const value = rawFields[fieldName];
      if (value === null) {
        if (!field.optional) throw new CodecError(`${path}.${fieldName} may not be null`);
        target[fieldName] = null;
      } else {
        const validated = validateMaterialized(field.type, value, `${path}.${fieldName}`);
        if (field.const && field.default !== null) {
          const expected = materializeDefault(field.default);
          if (!sameValue(validated, expected)) throw new CodecError(`${path}.${fieldName} is const`);
        }
        target[fieldName] = validated;
      }
      present.add(fieldName);
      continue;
    }
    if (field.default !== null) target[fieldName] = materializeDefault(field.default);
    else throw new CodecError(`${path}.${fieldName} is required`);
  }
  Object.defineProperty(target, PRESENT_FIELDS, { value: present, enumerable: false });

  return new Proxy(target, {
    set(object, property, value) {
      if (property === "$model") throw new TypeError("$model is immutable");
      if (typeof property === "string" && allowed.has(property)) present.add(property);
      return Reflect.set(object, property, value);
    },
    deleteProperty(object, property) {
      if (property === "$model") throw new TypeError("$model is immutable");
      if (typeof property === "string" && allowed.has(property)) present.delete(property);
      return Reflect.deleteProperty(object, property);
    },
  }) as unknown as OCCIDValue;
}

function makeAtomicModel(name: ModelName, value: unknown, path: string): OCCIDValue {
  const spec = MODEL_REGISTRY[name];
  if (!spec.atomic || !spec.valueType) throw new CodecError(`${name} is not atomic`);
  return { $model: name, value: validateMaterialized(spec.valueType, value, `${path}.value`) } as OCCIDValue;
}

export function createModel<N extends ModelName>(name: N, input: ModelInputMap[N]): ExactModelMap[N] {
  const spec = MODEL_REGISTRY[name];
  const result = spec.atomic
    ? makeAtomicModel(name, input, name)
    : makeRecordModel(name, input as unknown as StringMap<unknown>, name);
  return result as ExactModelMap[N];
}

function isOccidValue(value: unknown): value is OCCIDValue {
  return isPlainObject(value) && typeof value.$model === "string" && hasOwn(MODEL_REGISTRY, value.$model);
}

function isEnumValue(value: unknown): value is OCCIDEnumValue | OCCIDFlagValue {
  return isPlainObject(value) && typeof value.$enum === "string" && hasOwn(ENUM_REGISTRY, value.$enum);
}

function sameValue(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (typeof a === "bigint" && typeof b === "number" && Number.isSafeInteger(b)) return a === BigInt(b);
  if (typeof b === "bigint" && typeof a === "number" && Number.isSafeInteger(a)) return BigInt(a) === b;
  if (isEnumValue(a) && isEnumValue(b)) return a.$enum === b.$enum && a.value === b.value;
  return false;
}

function decodeTaggedString(data: unknown, path: string): string {
  if (typeof data === "string") return data;
  if (isPlainObject(data) && exactKeys(data, ["$text"])) {
    return decodeUtf8SurrogatePass(hexToBytes(data.$text, `${path}.$text`), path);
  }
  throw new CodecError(`${path} requires a string`);
}

function decodeTaggedInteger(data: unknown, path: string): OCCIDInteger {
  if (isSafeIntegerNumber(data)) return data;
  if (isPlainObject(data) && exactKeys(data, ["$integer"])) {
    const text = data.$integer;
    if (typeof text !== "string" || !/^-?(?:0|[1-9][0-9]*)$/.test(text))
      throw new CodecError(`${path}.$integer requires a decimal integer string`);
    return BigInt(text);
  }
  throw new CodecError(`${path} requires an integer; large integers require $integer`);
}

function decodeBytes(data: unknown, path: string): Uint8Array {
  if (!isPlainObject(data) || !exactKeys(data, ["$bytes"]))
    throw new CodecError(`${path} requires $bytes`);
  return hexToBytes(data.$bytes, `${path}.$bytes`);
}

function decodeEnum(data: unknown, expected: EnumName | null, path: string): OCCIDEnumValue | OCCIDFlagValue {
  if (!isPlainObject(data) || typeof data.enum !== "string" || !hasOwn(ENUM_REGISTRY, data.enum))
    throw new CodecError(`${path} requires a known OCCID enum`);
  const enumName = data.enum as EnumName;
  if (expected !== null && enumName !== expected) throw new CodecError(`${path} requires enum ${expected}`);
  const spec = ENUM_REGISTRY[enumName];
  if (spec.flags) {
    if (!exactKeys(data, ["enum", "names"]) || !Array.isArray(data.names) || data.names.some((name) => typeof name !== "string"))
      throw new CodecError(`${path} requires enum/names flag form`);
    let value = 0;
    const names: string[] = [];
    for (const name of data.names as string[]) {
      if (!hasOwn(spec.members, name)) throw new CodecError(`${path} has unknown ${enumName} flag ${name}`);
      const raw = spec.members[name];
      if (typeof raw !== "number") throw new CodecError(`${enumName}.${name} is not numeric`);
      value |= raw;
      names.push(name);
    }
    return flagValue(enumName, names, value);
  }
  if (!exactKeys(data, ["enum", "name"]) || typeof data.name !== "string" || !hasOwn(spec.members, data.name))
    throw new CodecError(`${path} requires enum/name form`);
  return enumValue(enumName, data.name, spec.members[data.name]);
}

function decodeByType(spec: TypeSpec, data: unknown, path: string): unknown {
  switch (spec.kind) {
    case "primitive":
      switch (spec.name) {
        case "string": return decodeTaggedString(data, path);
        case "bool": if (typeof data !== "boolean") throw new CodecError(`${path} requires boolean`); return data;
        case "float": return finiteNumber(data, path);
        case "int": case "int8": case "int16": case "int32": case "int64":
        case "uint8": case "uint16": case "uint32": case "uint64": return decodeTaggedInteger(data, path);
        case "bytes": return decodeBytes(data, path);
        case "any": return fromData(data, path);
      }
    case "fixedBytes": {
      const value = decodeBytes(data, path);
      if (value.length !== spec.size) throw new CodecError(`${path} requires exactly ${spec.size} bytes`);
      return value;
    }
    case "enum": return decodeEnum(data, spec.name, path);
    case "model": {
      const value = decodeModel(data, path);
      if (!isA(value, spec.name)) throw new CodecError(`${path} model ${value.$model} is not semantic ${spec.name}`);
      return value;
    }
    case "namespacedIntID": {
      const value = decodeModel(data, path);
      if (!isA(value, "IntID")) throw new CodecError(`${path} requires IntID(${spec.namespace})`);
      return value;
    }
    case "list":
      if (!Array.isArray(data)) throw new CodecError(`${path} requires list`);
      return data.map((item, index) => decodeByType(spec.item, item, `${path}[${index}]`));
    case "map": {
      const out = new Map<unknown, unknown>();
      if (isPlainObject(data) && !Object.keys(data).some((key) => RESERVED_TAGS.has(key))) {
        let index = 0;
        for (const [key, value] of Object.entries(data)) {
          const decodedKey = decodeByType(spec.key, key, `${path}.key[${index}]`);
          out.set(decodedKey, decodeByType(spec.value, value, `${path}.value[${index}]`));
          index++;
        }
        return out;
      }
      if (!isPlainObject(data) || !exactKeys(data, ["$map"]) || !Array.isArray(data.$map))
        throw new CodecError(`${path} requires a named map`);
      let index = 0;
      for (const pair of data.$map) {
        if (!Array.isArray(pair) || pair.length !== 2) throw new CodecError(`${path} map entries require pairs`);
        const key = decodeByType(spec.key, pair[0], `${path}.key[${index}]`);
        if (out.has(key)) throw new CodecError(`${path} has duplicate map key`);
        out.set(key, decodeByType(spec.value, pair[1], `${path}.value[${index}]`));
        index++;
      }
      return out;
    }
    case "tuple":
      if (!isPlainObject(data) || !exactKeys(data, ["$tuple"]) || !Array.isArray(data.$tuple) || data.$tuple.length !== spec.items.length)
        throw new CodecError(`${path} requires a ${spec.items.length}-item named tuple`);
      return tuple(...spec.items.map((itemSpec, index) => decodeByType(itemSpec, (data.$tuple as unknown[])[index], `${path}[${index}]`)));
    case "union": {
      let last: unknown = null;
      for (const item of spec.items) {
        try { return decodeByType(item, data, path); }
        catch (error) { last = error; }
      }
      throw last instanceof Error ? last : new CodecError(`${path} does not satisfy any union member`);
    }
  }
}

function decodeModel(data: unknown, path: string): OCCIDValue {
  if (!isPlainObject(data) || !exactKeys(data, ["model", "value"]) || typeof data.model !== "string" || !hasOwn(MODEL_REGISTRY, data.model))
    throw new CodecError(`${path} requires a known named OCCID model`);
  const name = data.model as ModelName;
  const spec = MODEL_REGISTRY[name];
  if (spec.atomic) {
    if (!spec.valueType) throw new CodecError(`${name} has no atomic value type`);
    let value: unknown;
    if (spec.valueType.kind === "primitive" && spec.valueType.name === "bytes") value = hexToBytes(data.value, `${path}.value`);
    else if (spec.valueType.kind === "fixedBytes") {
      value = hexToBytes(data.value, `${path}.value`);
      if ((value as Uint8Array).length !== spec.valueType.size) throw new CodecError(`${path}.value requires exactly ${spec.valueType.size} bytes`);
    } else value = decodeByType(spec.valueType, data.value, `${path}.value`);
    return makeAtomicModel(name, value, path);
  }
  if (!isPlainObject(data.value)) throw new CodecError(`${path}.${name}.value requires named fields`);
  const raw: StringMap<unknown> = {};
  for (const [key, item] of Object.entries(data.value)) {
    const field = spec.fields[key];
    if (!field) throw new CodecError(`${path}.${name}.${key} is not a field`);
    if (item === null) {
      if (!field.optional) throw new CodecError(`${path}.${name}.${key} may not be null`);
      raw[key] = null;
    } else raw[key] = decodeByType(field.type, item, `${path}.${name}.${key}`);
  }
  return makeRecordModel(name, raw, `${path}.${name}`);
}

export function fromData(data: unknown, path = "$root"): unknown {
  if (data === null || typeof data === "boolean" || typeof data === "string") return data;
  if (typeof data === "number") {
    if (!Number.isFinite(data)) throw new CodecError(`${path} contains non-finite number`);
    if (Number.isInteger(data) && !Number.isSafeInteger(data)) throw new CodecError(`${path} large integers require $integer`);
    return data;
  }
  if (Array.isArray(data)) return data.map((item, index) => fromData(item, `${path}[${index}]`));
  if (!isPlainObject(data)) throw new CodecError(`${path} contains unsupported value`);
  if (hasOwn(data, "model")) return decodeModel(data, path);
  if (hasOwn(data, "enum")) return decodeEnum(data, null, path);
  if (exactKeys(data, ["$bytes"])) return decodeBytes(data, path);
  if (exactKeys(data, ["$text"])) return decodeTaggedString(data, path);
  if (exactKeys(data, ["$integer"])) return decodeTaggedInteger(data, path);
  if (exactKeys(data, ["$tuple"]) && Array.isArray(data.$tuple))
    return tuple(...data.$tuple.map((item, index) => fromData(item, `${path}[${index}]`)));
  if (exactKeys(data, ["$map"]) && Array.isArray(data.$map)) {
    const out = new Map<unknown, unknown>();
    let index = 0;
    for (const pair of data.$map) {
      if (!Array.isArray(pair) || pair.length !== 2) throw new CodecError(`${path} map entries require pairs`);
      const key = fromData(pair[0], `${path}.key[${index}]`);
      if (out.has(key)) throw new CodecError(`${path} has duplicate map key`);
      out.set(key, fromData(pair[1], `${path}.value[${index}]`));
      index++;
    }
    return out;
  }
  if (Object.keys(data).some((key) => RESERVED_TAGS.has(key)))
    throw new CodecError(`${path} has malformed named tag; literal maps with tag keys require $map`);
  const out: StringMap<unknown> = {};
  for (const [key, value] of Object.entries(data)) out[key] = fromData(value, `${path}.${key}`);
  return out;
}

export function parseModel<N extends ModelName>(data: unknown, expected: N): SemanticModelMap[N] {
  const value = decodeModel(data, "$root");
  if (!isA(value, expected)) throw new CodecError(`${value.$model} is not semantically compatible with ${expected}`);
  return value as SemanticModelMap[N];
}

export function parseExactModel<N extends ModelName>(data: unknown, expected: N): ExactModelMap[N] {
  const value = decodeModel(data, "$root");
  if (value.$model !== expected) throw new CodecError(`expected concrete ${expected}, got ${value.$model}`);
  return value as ExactModelMap[N];
}

function encodeString(value: string): unknown {
  if (!containsUnsafeJsonText(value)) return value;
  return { $text: bytesToHex(encodeUtf8SurrogatePass(value)) };
}

function encodeInteger(value: OCCIDInteger): unknown {
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new CodecError("integer number is not safe; use bigint");
    return value;
  }
  const limit = BigInt(SAFE_INTEGER);
  return value >= -limit && value <= limit ? Number(value) : { $integer: value.toString(10) };
}

function encodeEnum(value: OCCIDEnumValue | OCCIDFlagValue): unknown {
  if (value.$flags === true) return { enum: value.$enum, names: [...value.names] };
  return { enum: value.$enum, name: value.name };
}

function encodeByType(spec: TypeSpec, value: unknown, path: string): unknown {
  switch (spec.kind) {
    case "primitive":
      switch (spec.name) {
        case "string": return encodeString(validatePrimitive("string", value, path) as string);
        case "bool": return validatePrimitive("bool", value, path);
        case "float": return validatePrimitive("float", value, path);
        case "int": case "int8": case "int16": case "int32": case "int64":
        case "uint8": case "uint16": case "uint32": case "uint64":
          return encodeInteger(validatePrimitive(spec.name, value, path) as OCCIDInteger);
        case "bytes": return { $bytes: bytesToHex(validatePrimitive("bytes", value, path) as Uint8Array) };
        case "any": return toData(value, path);
      }
    case "fixedBytes": {
      const bytes = validateMaterialized(spec, value, path) as Uint8Array;
      return { $bytes: bytesToHex(bytes) };
    }
    case "enum": {
      const e = validateMaterialized(spec, value, path) as OCCIDEnumValue | OCCIDFlagValue;
      return encodeEnum(e);
    }
    case "model": case "namespacedIntID":
      return encodeModel(validateMaterialized(spec, value, path) as OCCIDValue, path);
    case "list": {
      const items = validateMaterialized(spec, value, path) as unknown[];
      return items.map((item, index) => encodeByType(spec.item, item, `${path}[${index}]`));
    }
    case "map": {
      const map = validateMaterialized(spec, value, path) as Map<unknown, unknown>;
      const pairs: unknown[][] = [];
      let canObject = true;
      const object: StringMap<unknown> = {};
      let index = 0;
      for (const [key, item] of map) {
        const encodedKey = encodeByType(spec.key, key, `${path}.key[${index}]`);
        const encodedValue = encodeByType(spec.value, item, `${path}.value[${index}]`);
        pairs.push([encodedKey, encodedValue]);
        if (typeof encodedKey !== "string" || RESERVED_TAGS.has(encodedKey) || hasOwn(object, encodedKey)) canObject = false;
        else object[encodedKey] = encodedValue;
        index++;
      }
      return canObject ? object : { $map: pairs };
    }
    case "tuple": {
      const items = validateMaterialized(spec, value, path) as unknown[];
      return { $tuple: items.map((item, index) => encodeByType(spec.items[index], item, `${path}[${index}]`)) };
    }
    case "union": {
      let last: unknown = null;
      for (const item of spec.items) {
        try { return encodeByType(item, value, path); }
        catch (error) { last = error; }
      }
      throw last instanceof Error ? last : new CodecError(`${path} does not satisfy any union member`);
    }
  }
}

function encodeModel(value: OCCIDValue, path: string): unknown {
  const spec = MODEL_REGISTRY[value.$model];
  if (spec.atomic) {
    if (!spec.valueType || !hasOwn(value as object, "value")) throw new CodecError(`${path} atomic model is malformed`);
    const raw = (value as OCCIDAtomicValue).value;
    if ((spec.valueType.kind === "primitive" && spec.valueType.name === "bytes") || spec.valueType.kind === "fixedBytes") {
      const bytes = validateMaterialized(spec.valueType, raw, `${path}.value`) as Uint8Array;
      return { model: value.$model, value: bytesToHex(bytes) };
    }
    return { model: value.$model, value: encodeByType(spec.valueType, raw, `${path}.value`) };
  }

  const output: StringMap<unknown> = {};
  const fieldsSet = (value as unknown as { [PRESENT_FIELDS]?: globalThis.Set<string> })[PRESENT_FIELDS];
  const included = fieldsSet ?? new Set(spec.fieldOrder.filter((name) => hasOwn(value as object, name)));
  for (const fieldName of spec.fieldOrder) {
    if (!included.has(fieldName)) continue;
    const field = spec.fields[fieldName];
    const raw = (value as unknown as StringMap<unknown>)[fieldName];
    if (raw === null) {
      if (!field.optional) throw new CodecError(`${path}.${fieldName} may not be null`);
      output[fieldName] = null;
    } else output[fieldName] = encodeByType(field.type, raw, `${path}.${fieldName}`);
  }
  return { model: value.$model, value: output };
}

export function toData(value: unknown, path = "$root"): unknown {
  if (isOccidValue(value)) return encodeModel(value, path);
  if (isEnumValue(value)) return encodeEnum(value);
  if (value === null || typeof value === "boolean") return value;
  if (typeof value === "string") return encodeString(value);
  if (typeof value === "bigint") return encodeInteger(value);
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new CodecError(`${path} contains non-finite number`);
    if (Number.isInteger(value)) return encodeInteger(value);
    return value;
  }
  if (value instanceof Uint8Array) return { $bytes: bytesToHex(value) };
  if (isTupleValue(value)) return { $tuple: (value as unknown[]).map((item, index) => toData(item, `${path}[${index}]`)) };
  if (Array.isArray(value)) return value.map((item, index) => toData(item, `${path}[${index}]`));
  if (value instanceof Map) {
    const pairs: unknown[][] = [];
    let canObject = true;
    const object: StringMap<unknown> = {};
    let index = 0;
    for (const [key, item] of value) {
      const encodedKey = toData(key, `${path}.key[${index}]`);
      const encodedValue = toData(item, `${path}.value[${index}]`);
      pairs.push([encodedKey, encodedValue]);
      if (typeof encodedKey !== "string" || RESERVED_TAGS.has(encodedKey) || hasOwn(object, encodedKey)) canObject = false;
      else object[encodedKey] = encodedValue;
      index++;
    }
    return canObject ? object : { $map: pairs };
  }
  if (isPlainObject(value)) {
    const entries = Object.entries(value);
    if (entries.every(([key]) => !RESERVED_TAGS.has(key))) {
      const out: StringMap<unknown> = {};
      for (const [key, item] of entries) out[key] = toData(item, `${path}.${key}`);
      return out;
    }
    return { $map: entries.map(([key, item], index) => [toData(key, `${path}.key[${index}]`), toData(item, `${path}.value[${index}]`)]) };
  }
  throw new CodecError(`${path} contains unsupported value ${Object.prototype.toString.call(value)}`);
}


export type WireEnvelope = [number, unknown];

function enumFromWire(enumName: EnumName, raw: unknown, path: string): OCCIDEnumValue | OCCIDFlagValue {
  const spec = ENUM_REGISTRY[enumName];
  if (spec.flags) {
    if (typeof raw !== "number" || !Number.isInteger(raw)) throw new CodecError(`${path} requires numeric flag value`);
    const names: string[] = [];
    let known = 0;
    for (const [name, value] of Object.entries(spec.members)) {
      if (typeof value !== "number" || value === 0) continue;
      if ((raw & value) === value) { names.push(name); known |= value; }
    }
    if (known !== raw) throw new CodecError(`${path} contains unnamed ${enumName} flag bits`);
    return flagValue(enumName, names, raw);
  }
  for (const [name, value] of Object.entries(spec.members)) {
    if (value === raw) return enumValue(enumName, name, value);
  }
  throw new CodecError(`${path} has invalid ${enumName} value`);
}

function wireMapEntries(data: unknown, path: string): Array<[unknown, unknown]> {
  if (data instanceof Map) return [...data.entries()];
  if (isPlainObject(data)) return Object.entries(data);
  throw new CodecError(`${path} requires a map`);
}

function wireEncodeAny(value: unknown, path: string): unknown {
  if (isOccidValue(value)) return toWireEnvelope(value);
  if (isEnumValue(value)) return value.value;
  if (value === null || typeof value === "boolean" || typeof value === "string") return value;
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new CodecError(`${path} contains non-finite number`);
    return value;
  }
  if (typeof value === "bigint") return value;
  if (value instanceof Uint8Array) return value;
  if (Array.isArray(value)) return value.map((item, index) => wireEncodeAny(item, `${path}[${index}]`));
  if (value instanceof Map) {
    const out = new Map<unknown, unknown>();
    let index = 0;
    for (const [key, item] of value) {
      out.set(wireEncodeAny(key, `${path}.key[${index}]`), wireEncodeAny(item, `${path}.value[${index}]`));
      index++;
    }
    return out;
  }
  if (isPlainObject(value)) {
    const out: StringMap<unknown> = {};
    for (const [key, item] of Object.entries(value)) out[key] = wireEncodeAny(item, `${path}.${key}`);
    return out;
  }
  throw new CodecError(`${path} contains unsupported compact-wire value`);
}

function wireEncodeType(spec: TypeSpec, value: unknown, path: string): unknown {
  switch (spec.kind) {
    case "primitive":
      if (spec.name === "any") return wireEncodeAny(value, path);
      return validatePrimitive(spec.name, value, path);
    case "fixedBytes": return validateMaterialized(spec, value, path);
    case "enum": return (validateMaterialized(spec, value, path) as OCCIDEnumValue | OCCIDFlagValue).value;
    case "model": {
      const actual = validateMaterialized(spec, value, path) as OCCIDValue;
      const actualSpec = MODEL_REGISTRY[actual.$model];
      if (actual.$model === spec.name && actualSpec.atomic && actualSpec.valueType) {
        return wireEncodeType(actualSpec.valueType, (actual as OCCIDAtomicValue).value, `${path}.value`);
      }
      return toWireEnvelope(actual);
    }
    case "namespacedIntID": {
      const actual = validateMaterialized(spec, value, path) as OCCIDValue;
      const actualSpec = MODEL_REGISTRY[actual.$model];
      if (actual.$model === "IntID" && actualSpec.atomic && actualSpec.valueType)
        return wireEncodeType(actualSpec.valueType, (actual as OCCIDAtomicValue).value, `${path}.value`);
      return toWireEnvelope(actual);
    }
    case "list":
      return (validateMaterialized(spec, value, path) as unknown[])
        .map((item, index) => wireEncodeType(spec.item, item, `${path}[${index}]`));
    case "map": {
      const input = validateMaterialized(spec, value, path) as Map<unknown, unknown>;
      const out = new Map<unknown, unknown>();
      let index = 0;
      for (const [key, item] of input) {
        out.set(wireEncodeType(spec.key, key, `${path}.key[${index}]`), wireEncodeType(spec.value, item, `${path}.value[${index}]`));
        index++;
      }
      return out;
    }
    case "tuple": {
      const input = validateMaterialized(spec, value, path) as unknown[];
      return input.map((item, index) => wireEncodeType(spec.items[index], item, `${path}[${index}]`));
    }
    case "union": {
      let last: unknown = null;
      for (const item of spec.items) {
        try { return wireEncodeType(item, value, path); }
        catch (error) { last = error; }
      }
      throw last instanceof Error ? last : new CodecError(`${path} does not satisfy any compact-wire union member`);
    }
  }
}

function wireDecodeAny(data: unknown, path: string): unknown {
  if (Array.isArray(data) && data.length === 2 && typeof data[0] === "number" && hasOwn(MODEL_NAME_BY_ID, data[0]))
    return fromWireEnvelope(data);
  if (data === null || typeof data === "boolean" || typeof data === "string" || typeof data === "bigint") return data;
  if (typeof data === "number") {
    if (!Number.isFinite(data)) throw new CodecError(`${path} contains non-finite number`);
    return data;
  }
  if (data instanceof Uint8Array) return data;
  if (Array.isArray(data)) return data.map((item, index) => wireDecodeAny(item, `${path}[${index}]`));
  if (data instanceof Map) {
    const out = new Map<unknown, unknown>();
    let index = 0;
    for (const [key, item] of data) {
      out.set(wireDecodeAny(key, `${path}.key[${index}]`), wireDecodeAny(item, `${path}.value[${index}]`));
      index++;
    }
    return out;
  }
  if (isPlainObject(data)) {
    const out: StringMap<unknown> = {};
    for (const [key, item] of Object.entries(data)) out[key] = wireDecodeAny(item, `${path}.${key}`);
    return out;
  }
  throw new CodecError(`${path} contains unsupported compact-wire value`);
}

function wireDecodeType(spec: TypeSpec, data: unknown, path: string): unknown {
  switch (spec.kind) {
    case "primitive":
      if (spec.name === "any") return wireDecodeAny(data, path);
      return validatePrimitive(spec.name, data, path);
    case "fixedBytes": return validateMaterialized(spec, data, path);
    case "enum": return enumFromWire(spec.name, data, path);
    case "model": {
      if (Array.isArray(data) && data.length === 2 && typeof data[0] === "number") {
        const actual = fromWireEnvelope(data);
        if (!isA(actual, spec.name)) throw new CodecError(`${path} model ${actual.$model} is not semantic ${spec.name}`);
        return actual;
      }
      const expected = MODEL_REGISTRY[spec.name];
      if (!expected.atomic || !expected.valueType)
        throw new CodecError(`${path} nested semantic ${spec.name} requires [model_id,payload]`);
      return makeAtomicModel(spec.name, wireDecodeType(expected.valueType, data, `${path}.value`), path);
    }
    case "namespacedIntID": {
      if (Array.isArray(data) && data.length === 2 && typeof data[0] === "number") {
        const actual = fromWireEnvelope(data);
        if (!isA(actual, "IntID")) throw new CodecError(`${path} requires IntID(${spec.namespace})`);
        return actual;
      }
      const expected = MODEL_REGISTRY.IntID;
      if (!expected.atomic || !expected.valueType) throw new CodecError("IntID is not atomic");
      return makeAtomicModel("IntID", wireDecodeType(expected.valueType, data, `${path}.value`), path);
    }
    case "list":
      if (!Array.isArray(data)) throw new CodecError(`${path} requires compact-wire list`);
      return data.map((item, index) => wireDecodeType(spec.item, item, `${path}[${index}]`));
    case "map": {
      const out = new Map<unknown, unknown>();
      let index = 0;
      for (const [key, item] of wireMapEntries(data, path)) {
        out.set(wireDecodeType(spec.key, key, `${path}.key[${index}]`), wireDecodeType(spec.value, item, `${path}.value[${index}]`));
        index++;
      }
      return out;
    }
    case "tuple":
      if (!Array.isArray(data) || data.length !== spec.items.length)
        throw new CodecError(`${path} requires ${spec.items.length}-item compact-wire tuple`);
      return tuple(...spec.items.map((itemSpec, index) => wireDecodeType(itemSpec, data[index], `${path}[${index}]`)));
    case "union": {
      let last: unknown = null;
      for (const item of spec.items) {
        try { return wireDecodeType(item, data, path); }
        catch (error) { last = error; }
      }
      throw last instanceof Error ? last : new CodecError(`${path} does not satisfy any compact-wire union member`);
    }
  }
}

export function toWireEnvelope(value: OCCIDValue): WireEnvelope {
  const spec = MODEL_REGISTRY[value.$model];
  if (spec.atomic) {
    if (!spec.valueType) throw new CodecError(`${value.$model} has no atomic value type`);
    return [spec.id, wireEncodeType(spec.valueType, (value as OCCIDAtomicValue).value, `${value.$model}.value`)];
  }
  const fields = new Map<number, unknown>();
  const present = modelFieldsSet(value);
  for (let ordinal = 0; ordinal < spec.fieldOrder.length; ordinal++) {
    const name = spec.fieldOrder[ordinal];
    if (!present.has(name)) continue;
    const field = spec.fields[name];
    const raw = (value as unknown as StringMap<unknown>)[name];
    if (raw === null) {
      if (!field.optional) throw new CodecError(`${value.$model}.${name} may not be null`);
      fields.set(ordinal, null);
    } else {
      // Python's generated runtime represents an optional field as a Union[T, None].
      // Its compact encoder therefore has no direct T annotation at this layer and
      // encodes present non-null values through the generic value path. Preserve that
      // observable wire behavior, especially for optional OCCIDValue fields.
      fields.set(
        ordinal,
        field.optional
          ? wireEncodeAny(raw, `${value.$model}.${name}`)
          : wireEncodeType(field.type, raw, `${value.$model}.${name}`),
      );
    }
  }
  return [spec.id, fields];
}

export function fromWireEnvelope(envelope: unknown): OCCIDValue {
  if (!Array.isArray(envelope) || envelope.length !== 2 || typeof envelope[0] !== "number" || !Number.isInteger(envelope[0]))
    throw new CodecError("OCCID compact wire requires [model_id,payload]");
  const name = MODEL_NAME_BY_ID[envelope[0]];
  if (!name) throw new CodecError(`unknown OCCID model ID ${envelope[0]}`);
  const spec = MODEL_REGISTRY[name];
  if (spec.atomic) {
    if (!spec.valueType) throw new CodecError(`${name} has no atomic value type`);
    return makeAtomicModel(name, wireDecodeType(spec.valueType, envelope[1], `${name}.value`), name);
  }
  const rawFields: StringMap<unknown> = {};
  for (const [rawOrdinal, rawValue] of wireMapEntries(envelope[1], name)) {
    const ordinal = typeof rawOrdinal === "number" ? rawOrdinal : Number(rawOrdinal);
    if (!Number.isInteger(ordinal) || ordinal < 0 || ordinal >= spec.fieldOrder.length)
      throw new CodecError(`invalid field ordinal ${String(rawOrdinal)} for ${name}`);
    const fieldName = spec.fieldOrder[ordinal];
    const field = spec.fields[fieldName];
    if (rawValue === null) {
      if (!field.optional) throw new CodecError(`${name}.${fieldName} may not be null`);
      rawFields[fieldName] = null;
    } else rawFields[fieldName] = wireDecodeType(field.type, rawValue, `${name}.${fieldName}`);
  }
  return makeRecordModel(name, rawFields, name);
}

export function dumps(value: unknown, space?: number): string {
  return JSON.stringify(toData(value), null, space);
}

export function loads(text: string): unknown {
  // JSON.parse, unlike Python's object_pairs_hook, cannot report duplicate keys.
  // HTTP JSON parsers have the same limitation.  All post-parse OCCID validation
  // is strict and rejects malformed named tags and extra model fields.
  return fromData(JSON.parse(text));
}
'''


def render_maps(modules: list[idl.ModuleDef]) -> str:
    enum_names = {e.name for module in modules for e in module.enums}
    model_names = {m.name for module in modules for m in module.models}
    blocks = ["// Generated schema maps"]
    for module in sorted(modules, key=lambda m: m.name):
        for mapping in sorted(module.maps, key=lambda m: m.name):
            key_node = idl.TypeParser(mapping.key_type).parse()
            value_node = idl.TypeParser(mapping.value_type).parse()
            key_type = ts_type(key_node, model_names, enum_names)
            value_type = ts_type(value_node, model_names, enum_names)
            entries = []
            for key, value in mapping.entries.items():
                if mapping.key_type in enum_names:
                    key_expr = f"{mapping.key_type}.{key}"
                else:
                    key_expr = q(key)
                if mapping.value_type in enum_names:
                    value_expr = f"{mapping.value_type}.{value}"
                else:
                    value_expr = q(value)
                entries.append(f"  [{key_expr}, {value_expr}],")
            blocks.append(
                f"export const {mapping.name}: ReadonlyMap<{key_type}, {value_type}> = new Map<{key_type}, {value_type}>([\n"
                + "\n".join(entries) + "\n]);"
            )
    return "\n\n".join(blocks)


def render_contract_symbols(contract_path: Path) -> str:
    if not contract_path.is_file():
        return "export const OCCID_SYMBOL_HASHES: Readonly<StringMap<string>> = Object.freeze({});"
    data = json.loads(contract_path.read_text(encoding="utf-8"))
    symbols = data.get("symbols")
    if not isinstance(symbols, dict):
        return "export const OCCID_SYMBOL_HASHES: Readonly<StringMap<string>> = Object.freeze({});"
    hashes = {
        name: entry.get("hash")
        for name, entry in symbols.items()
        if isinstance(name, str) and isinstance(entry, dict) and isinstance(entry.get("hash"), str)
    }
    return "export const OCCID_SYMBOL_HASHES: Readonly<StringMap<string>> = Object.freeze(" + q(hashes) + ");"


def render(modules: list[idl.ModuleDef], version: str, contract_path: Path) -> str:
    symbol_index = idl.build_symbol_index(modules)
    enum_members = idl.build_enum_members(modules)
    idl.validate_schema(modules, symbol_index, enum_members)

    contract_hash: str | None = None
    if contract_path.is_file():
        try:
            data = json.loads(contract_path.read_text(encoding="utf-8"))
            value = data.get("global_hash")
            if isinstance(value, str):
                contract_hash = value
        except json.JSONDecodeError as exc:
            raise GenerationError(f"invalid contract marker {contract_path}: {exc}") from exc

    sections = [
        render_runtime_header(version, contract_hash),
        render_enums(modules),
        render_models(modules),
        render_enum_registry(modules),
        render_model_registry(modules),
        render_contract_symbols(contract_path),
        render_runtime_body(),
        render_maps(modules),
    ]
    return "\n\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    modules = idl.load_compiled_schema(args.input)
    version = args.version_file.read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit(f"empty VERSION: {args.version_file}")
    output = render(modules, version, args.contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Generated TypeScript OCCID binding: {args.output}")


if __name__ == "__main__":
    main()
