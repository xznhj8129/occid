"""Compact model-ID/field-ordinal MsgPack; field presence is preserved."""
from __future__ import annotations

from enum import Enum
from types import UnionType
from typing import Annotated, get_args, get_origin

import msgpack

from .runtime import SemanticModel, SemanticRegistry, UID, value_semantics


def _wire_value(value):
    if isinstance(value, SemanticModel):
        validated = type(value)(**{name: getattr(value, name) for name in type(value).model_fields})
        fields = {
            index: _wire_value(getattr(validated, name))
            for index, name in enumerate(type(value).model_fields)
            if name in value.model_fields_set
            or getattr(value, name) != type(value).model_fields[name].get_default(call_default_factory=True)
        }
        return [type(value)._model_id, fields]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, UID):
        return bytes(value)
    if isinstance(value, list):
        return [_wire_value(item) for item in value]
    return value


def encode(value: SemanticModel) -> bytes:
    if not isinstance(value, SemanticModel):
        raise TypeError("encode requires a semantic model")
    return msgpack.packb(_wire_value(value), use_bin_type=True)


def _unique_map(pairs):
    result = {}
    for key, value in pairs:
        if type(key) is not int or key in result:
            raise ValueError(f"invalid or duplicate wire field ordinal {key!r}")
        result[key] = value
    return result


def _decode_value(annotation, value, registry: SemanticRegistry):
    origin = get_origin(annotation)
    if origin is Annotated:
        return _decode_value(get_args(annotation)[0], value, registry)
    if origin is UnionType:
        if value is None and type(None) in get_args(annotation):
            return None
        annotation = next(arg for arg in get_args(annotation) if arg is not type(None))
        return _decode_value(annotation, value, registry)
    if origin is list:
        if type(value) is not list:
            raise ValueError("wire collection must be a list")
        return [_decode_value(get_args(annotation)[0], item, registry) for item in value]
    if isinstance(annotation, type) and issubclass(annotation, SemanticModel):
        model = _decode_model(value, registry)
        if not registry.entails(value_semantics(model), annotation):
            raise ValueError(f"wire {type(model).__name__} does not satisfy {annotation.__name__}")
        return model
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        if type(value) is not int:
            raise ValueError("wire enum must be an integer")
        return annotation(value)
    return value


def _decode_model(envelope, registry: SemanticRegistry) -> SemanticModel:
    if type(envelope) is not list or len(envelope) != 2 or type(envelope[0]) is not int:
        raise ValueError("wire model must be [model_id, field_map]")
    model_id, raw_fields = envelope
    model = registry.model_types.get(model_id)
    if model is None:
        raise ValueError(f"unknown wire model ID {model_id}")
    if type(raw_fields) is not dict:
        raise ValueError(f"wire fields for {model.__name__} must be a numeric map")
    names = tuple(model.model_fields)
    values = {}
    for index, raw in raw_fields.items():
        if type(index) is not int or not 0 <= index < len(names):
            raise ValueError(f"invalid wire field ordinal {index!r} for {model.__name__}")
        name = names[index]
        values[name] = _decode_value(model.model_fields[name].annotation, raw, registry)
    return model(**values)


def decode(payload: bytes, registry: SemanticRegistry) -> SemanticModel:
    envelope = msgpack.unpackb(payload, raw=False, strict_map_key=False, object_pairs_hook=_unique_map)
    return _decode_model(envelope, registry)
