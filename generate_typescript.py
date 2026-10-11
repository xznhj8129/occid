"""Generate TypeScript data bindings from the compiled OCCID2 registry."""
from __future__ import annotations

import json
from pathlib import Path


def ts_type(text: str, models: dict, enums: dict) -> str:
    if text.startswith("optional "):
        return ts_type(text[9:], models, enums) + " | null"
    if text.startswith("list[") and text.endswith("]"):
        return "Array<" + ts_type(text[5:-1], models, enums) + ">"
    if text in models:
        return text
    if text in enums:
        return text
    return {"string": "string", "float": "number", "int": "number | bigint", "bool": "boolean", "UID": "UID"}[text]


def generate_typescript(registry: dict, output: Path) -> None:
    lines = [
        "// GENERATED FILE - DO NOT EDIT",
        "export type UID = Uint8Array; // Runtime representation: exactly 16 bytes.",
        "",
    ]
    for name, members in registry["enums"].items():
        lines.append(f"export enum {name} {{")
        lines.extend(f"  {member} = {value}," for member, value in members.items())
        lines.extend(["}", ""])
    for name, spec in registry["axes"].items():
        values = {value: f"{name}.{value}" for value in spec["values"]}
        lines.append(f"export const {name} = {json.dumps(values)} as const;")
    for name, terms in registry["aliases"].items():
        lines.append(f"export const {name} = {json.dumps(terms)} as const;")
    for name, spec in registry["expressions"].items():
        lines.append(f"export const {name} = {json.dumps(spec)} as const;")
    lines.append("")
    for name, spec in registry["models"].items():
        lines.append(f"export interface {name} {{")
        for field in spec["effective_fields"]:
            text = field["type"]
            optional = text.startswith(("optional ", "list[")) or field["default"] is not None
            suffix = "?" if optional else ""
            lines.append(f"  {field['name']}{suffix}: {ts_type(text, registry['models'], registry['enums'])};")
        lines.extend(["}", ""])
    for name, spec in registry["relations"].items():
        lines.append(f"export const {name} = {json.dumps(spec)} as const;")
    model_ids = {name: spec["model_id"] for name, spec in sorted(registry["models"].items())}
    lines.append("export const MODEL_IDS = " + json.dumps(model_ids) + " as const;")
    output.write_text("\n".join(lines) + "\n")
