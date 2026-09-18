"""Lossless named OCCID JSON: ``loads(dumps(value))``.

This is a human/API codec. It never uses compact-wire model IDs. Record fields
retain their presence; each nested OCCID value retains its concrete name.
"""
from __future__ import annotations

import json
import math
import re
from enum import Enum, IntFlag
from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer, TypeAdapter, ValidationError, WithJsonSchema

from . import schema
from .schema.common import OCCIDModel, OCCIDValue, OCCID_MODEL_BY_NAME

SAFE_INTEGER = 2**53 - 1
_TAGS = {"model", "enum", "$bytes", "$integer", "$map", "$tuple", "$text"}
_ENUMS = {
    name: value for name, value in vars(schema).items()
    if isinstance(value, type) and issubclass(value, Enum)
    and value.__module__.startswith("occid.schema.") and value.__members__
}


class CodecError(ValueError):
    """The named input is malformed or does not satisfy the current schema."""


def to_data(value):
    """Return JSON-safe data without losing scalar type or concrete meaning."""
    if isinstance(value, OCCIDValue):
        raw = value.root.hex() if isinstance(value.root, bytes) else to_data(value.root)
        return {"model": type(value).__name__, "value": raw}
    if isinstance(value, OCCIDModel):
        return {"model": type(value).__name__, "value": {
            name: to_data(getattr(value, name))
            for name in type(value).model_fields if name in value.model_fields_set
        }}
    if isinstance(value, IntFlag):
        members = [member for member in type(value) if member & value == member]
        if sum(int(member) for member in members) != int(value):
            raise CodecError(f"{type(value).__name__} has unnamed flag bits")
        return {"enum": type(value).__name__, "names": [m.name for m in members]}
    if isinstance(value, Enum):
        return {"enum": type(value).__name__, "name": value.name}
    if value is None or type(value) is bool:
        return value
    if type(value) is str:
        # JSONB cannot store NUL or isolated UTF-16 surrogates as JSON strings.
        if "\x00" in value or any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            return {"$text": value.encode("utf-8", "surrogatepass").hex()}
        return value
    if type(value) is int:
        return value if abs(value) <= SAFE_INTEGER else {"$integer": str(value)}
    if type(value) is float:
        if not math.isfinite(value):
            raise CodecError("non-finite numbers are not valid named OCCID JSON")
        return value
    if type(value) is bytes:
        return {"$bytes": value.hex()}
    if type(value) is list:
        return [to_data(item) for item in value]
    if type(value) is tuple:
        return {"$tuple": [to_data(item) for item in value]}
    if type(value) is dict:
        if all(type(key) is str and key not in _TAGS and to_data(key) == key for key in value):
            return {key: to_data(item) for key, item in value.items()}
        return {"$map": [[to_data(key), to_data(item)] for key, item in value.items()]}
    raise CodecError(f"unsupported named value: {type(value).__name__}")


def _hex(value):
    if type(value) is not str or re.fullmatch(r"(?:[0-9a-f]{2})*", value) is None:
        raise CodecError("binary values require an even number of lowercase hexadecimal digits")
    return bytes.fromhex(value)


def from_data(data):
    """Decode named data, then validate every model with the installed OCCID."""
    if type(data) is list:
        return [from_data(item) for item in data]
    if type(data) is not dict:
        if data is None or type(data) in (bool, str):
            return data
        if type(data) is int and abs(data) <= SAFE_INTEGER:
            return data
        if type(data) is float and math.isfinite(data):
            return data
        raise CodecError("invalid JSON scalar; large integers require $integer")
    keys = set(data)
    if "model" in data:
        if keys != {"model", "value"} or type(data["model"]) is not str:
            raise CodecError("a named model requires exactly model and value")
        model = OCCID_MODEL_BY_NAME.get(data["model"])
        if model is None:
            raise CodecError(f"unknown OCCID model {data['model']!r}")
        raw = data["value"]
        if issubclass(model, OCCIDValue):
            value = _hex(raw) if model.model_fields["root"].annotation is bytes else from_data(raw)
        else:
            if type(raw) is not dict:
                raise CodecError(f"{model.__name__} requires named fields")
            value = {key: from_data(item) for key, item in raw.items()}
        try:
            return model.model_validate(value)
        except ValidationError as exc:
            raise CodecError(str(exc)) from exc
    if "enum" in data:
        name = data["enum"]
        if type(name) is not str or name not in _ENUMS:
            raise CodecError(f"unknown OCCID enum {name!r}")
        enum = _ENUMS[name]
        if issubclass(enum, IntFlag) and keys == {"enum", "names"}:
            names = data["names"]
            if type(names) is not list or any(type(n) is not str or n not in enum.__members__ for n in names):
                raise CodecError(f"invalid {name} flag names")
            result = enum(0)
            for member in names:
                result |= enum[member]
            return result
        if keys != {"enum", "name"} or type(data["name"]) is not str or data["name"] not in enum.__members__:
            raise CodecError(f"invalid {name} member")
        return enum[data["name"]]
    if keys == {"$bytes"}:
        return _hex(data["$bytes"])
    if keys == {"$text"}:
        try:
            return _hex(data["$text"]).decode("utf-8", "surrogatepass")
        except UnicodeDecodeError as exc:
            raise CodecError("invalid encoded text") from exc
    if keys == {"$integer"}:
        value = data["$integer"]
        if type(value) is not str or re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value) is None:
            raise CodecError("$integer requires a decimal integer string")
        return int(value)
    if keys == {"$tuple"} and type(data["$tuple"]) is list:
        return tuple(from_data(item) for item in data["$tuple"])
    if keys == {"$map"} and type(data["$map"]) is list:
        result = {}
        for pair in data["$map"]:
            if type(pair) is not list or len(pair) != 2:
                raise CodecError("$map entries must be key/value pairs")
            key, value = map(from_data, pair)
            try:
                if key in result:
                    raise CodecError("duplicate map key")
                result[key] = value
            except TypeError as exc:
                raise CodecError("unhashable map key") from exc
        return result
    if keys & _TAGS:
        raise CodecError("malformed named tag; literal maps with tag keys require $map")
    return {key: from_data(value) for key, value in data.items()}


def dumps(value, *, indent=None):
    return json.dumps(to_data(value), ensure_ascii=True, allow_nan=False, indent=indent)


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CodecError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def loads(text):
    try:
        data = json.loads(text, object_pairs_hook=_unique_pairs)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CodecError(str(exc)) from exc
    return from_data(data)


class Named:
    """Pydantic boundary annotation: ``position: Named[LocationState]``.

    The extension carries the generated value schema. The envelope describes
    the named wire form; callers must use this codec, not Pydantic's bare JSON.
    """

    def __class_getitem__(cls, target):
        def validate(value):
            result = value if type(value) is target else from_data(value)
            if type(result) is not target:
                raise CodecError(f"expected concrete {target.__name__}")
            return result

        if issubclass(target, Enum):
            wire_schema = {"type": "object", "properties": {
                "enum": {"const": target.__name__},
                "name": {"type": "string", "enum": list(target.__members__)},
            }, "required": ["enum", "name"], "additionalProperties": False}
        else:
            wire_schema = {"type": "object", "properties": {
                "model": {"const": target.__name__}, "value": {},
            }, "required": ["model", "value"], "additionalProperties": False,
                "x-occid-value-schema": TypeAdapter(target).json_schema()}
        return Annotated[target, BeforeValidator(validate),
                         PlainSerializer(to_data, return_type=dict), WithJsonSchema(wire_schema)]
