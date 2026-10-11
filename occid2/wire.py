"""Named MsgPack facts with inline definitions or resolvable revision identity."""
from __future__ import annotations

import msgpack

from .runtime import Datum, Product, SemanticRegistry, SemanticValue, product_names, subject_identity

FORMAT = "occid2.fact/1"
FIELDS = {"format", "id", "subject", "semantics", "meaning", "definition_id", "definitions", "value", "source", "observed_at", "validity", "provenance", "partial", "unit"}
REQUIRED = {"format", "id", "subject", "semantics", "meaning", "definition_id", "value"}
VALUE_EXTENSION = 1
PRODUCT_EXTENSION = 2


def _semantic_extension(value):
    if isinstance(value, SemanticValue):
        body = {"format": "occid2.value/1", "semantics": list(value.semantics), "value": value.value, "partial": value.partial, "unit": value.unit}
        return msgpack.ExtType(VALUE_EXTENSION, msgpack.packb(body, use_bin_type=True, default=_semantic_extension))
    if isinstance(value, Product):
        return msgpack.ExtType(PRODUCT_EXTENSION, msgpack.packb({"format": "occid2.product/1", "terms": list(value)}, use_bin_type=True))
    raise TypeError(f"wire value is not serializable: {type(value).__name__}")


def _read_extension(code, data):
    if code not in (VALUE_EXTENSION, PRODUCT_EXTENSION):
        return msgpack.ExtType(code, data)
    body = msgpack.unpackb(data, raw=False, ext_hook=_read_extension, object_pairs_hook=_unique_map)
    if code == PRODUCT_EXTENSION and isinstance(body, dict) and body.get("format") == "occid2.product/1":
        return _product(body["terms"], "terms")
    if code == VALUE_EXTENSION and isinstance(body, dict) and body.get("format") == "occid2.value/1":
        if type(body.get("partial", False)) is not bool:
            raise ValueError("wire semantic value partial must be boolean")
        return SemanticValue(_product(body["semantics"], "semantics"), body["value"], body.get("partial", False), body.get("unit"))
    raise ValueError("invalid semantic wire extension")


def encode(value: Datum, *, include_definitions: bool = True) -> bytes:
    if not isinstance(value, Datum):
        raise TypeError("encode requires a semantic datum")
    if value.extensions.keys() & FIELDS:
        raise ValueError("fact extensions collide with envelope fields")
    envelope = {
        **value.extensions,
        "format": FORMAT,
        "id": value.id,
        "subject": value.subject,
        "semantics": list(value.semantics),
        "meaning": list(value.meaning),
        "definition_id": value.definition_id,
        "value": value.value,
        "source": value.source,
        "observed_at": value.observed_at,
        "validity": value.validity,
        "provenance": value.provenance,
        "partial": value.partial,
        "unit": value.unit,
    }
    if include_definitions:
        envelope["definitions"] = value.definitions
    return msgpack.packb(envelope, use_bin_type=True, default=_semantic_extension)


def _unique_map(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate wire key {key!r}")
        result[key] = value
    return result


def _product(raw, field: str) -> Product:
    if not isinstance(raw, list) or any(not isinstance(term, str) or not term for term in raw) or len(set(raw)) != len(raw):
        raise ValueError(f"wire {field} must be a list of distinct semantic names")
    return product_names(raw)


def decode(payload: bytes, *, registry: SemanticRegistry | None = None) -> Datum:
    envelope = msgpack.unpackb(payload, raw=False, strict_map_key=False, object_pairs_hook=_unique_map, ext_hook=_read_extension)
    if not isinstance(envelope, dict) or REQUIRED - envelope.keys():
        raise ValueError("wire fact is missing required named fields")
    if envelope["format"] != FORMAT:
        raise ValueError(f"unsupported wire format {envelope['format']!r}")
    if not isinstance(envelope["id"], str) or not envelope["id"]:
        raise ValueError("wire fact identity must be nonempty text")
    subject_identity(envelope["subject"])
    if "definitions" in envelope:
        registry = SemanticRegistry(envelope["definitions"])
    elif registry is not None:
        registry = registry.at(envelope["definition_id"])
    else:
        raise ValueError("wire fact requires inline definitions or a registry resolving its definition identity")
    if envelope["definition_id"] != registry.definition_id:
        raise ValueError("wire definition identity does not match its definitions")
    semantics = _product(envelope["semantics"], "semantics")
    meaning = _product(envelope["meaning"], "meaning")
    if not registry.legal(semantics) or registry.closure(semantics) != meaning:
        raise ValueError("wire fact meaning does not match its original definitions")
    partial = envelope.get("partial", False)
    if type(partial) is not bool:
        raise ValueError("wire partial must be boolean")
    unit = envelope.get("unit")
    if unit is not None and not isinstance(unit, str):
        raise ValueError("wire unit must be text")
    registry.validate_value(semantics, envelope["value"], partial=partial)
    provenance = envelope.get("provenance", {})
    if not isinstance(provenance, dict):
        raise ValueError("wire provenance must be a mapping")
    return Datum(envelope["id"], envelope["subject"], semantics, meaning, registry.definition_id, envelope["value"], registry._revision, envelope.get("source"), envelope.get("observed_at"), envelope.get("validity"), provenance, {key: value for key, value in envelope.items() if key not in FIELDS}, partial, unit)
