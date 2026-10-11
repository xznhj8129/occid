"""Self-describing MsgPack facts with named fields and definition snapshots."""
from __future__ import annotations

import msgpack

from .runtime import Datum, Product, SemanticRegistry, product_names, subject_identity

FORMAT = "occid2.fact/1"
FIELDS = {"format", "id", "subject", "semantics", "meaning", "definition_id", "definitions", "value", "source", "observed_at", "validity", "provenance"}
REQUIRED = {"format", "id", "subject", "semantics", "meaning", "definition_id", "definitions", "value"}


def encode(value: Datum) -> bytes:
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
        "definitions": value.definitions,
        "value": value.value,
        "source": value.source,
        "observed_at": value.observed_at,
        "validity": value.validity,
        "provenance": value.provenance,
    }
    return msgpack.packb(envelope, use_bin_type=True)


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


def decode(payload: bytes) -> Datum:
    envelope = msgpack.unpackb(payload, raw=False, strict_map_key=False, object_pairs_hook=_unique_map)
    if not isinstance(envelope, dict) or REQUIRED - envelope.keys():
        raise ValueError("wire fact is missing required named fields")
    if envelope["format"] != FORMAT:
        raise ValueError(f"unsupported wire format {envelope['format']!r}")
    if not isinstance(envelope["id"], str) or not envelope["id"]:
        raise ValueError("wire fact identity must be nonempty text")
    subject_identity(envelope["subject"])
    registry = SemanticRegistry(envelope["definitions"])
    if envelope["definition_id"] != registry.definition_id:
        raise ValueError("wire definition identity does not match its definitions")
    semantics = _product(envelope["semantics"], "semantics")
    meaning = _product(envelope["meaning"], "meaning")
    if not registry.legal(semantics) or registry.closure(semantics) != meaning:
        raise ValueError("wire fact meaning does not match its original definitions")
    registry.validate_value(semantics, envelope["value"])
    provenance = envelope.get("provenance", {})
    if not isinstance(provenance, dict):
        raise ValueError("wire provenance must be a mapping")
    return Datum(envelope["id"], envelope["subject"], semantics, meaning, registry.definition_id, envelope["value"], registry.spec, envelope.get("source"), envelope.get("observed_at"), envelope.get("validity"), provenance, {key: value for key, value in envelope.items() if key not in FIELDS})
