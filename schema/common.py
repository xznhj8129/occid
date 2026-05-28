"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, auto, Enum
from typing import Annotated, Any, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

SchemaVersion = tuple[int, int, int]

### Enums

class IntEnum(_StdIntEnum):
    @classmethod
    def _missing_(cls, value):
        if type(value) == str:
            return cls[value]
        return super()._missing_(value)

### Models

class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def encode(self) -> bytes:
        return msgpack.packb(self._wire_value(self), use_bin_type=True)

    @classmethod
    def decode(cls, payload: bytes):
        return cls._from_wire(msgpack.unpackb(payload, raw=False))

    @classmethod
    def _from_wire(cls, data):
        if type(data) == dict:
            return cls.model_validate(data)

        field_items = list(cls.model_fields.items())
        if len(data) > len(field_items):
            raise ValueError(f"{cls.__name__} wire data has too many fields")

        values = {}
        for index, item in enumerate(data):
            field_name, field_info = field_items[index]
            values[field_name] = cls._wire_to_value(field_info.annotation, item)
        return cls(**values)

    @classmethod
    def _wire_to_value(cls, annotation, data):
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is Annotated:
            return cls._wire_to_value(args[0], data)

        if origin is list:
            return [cls._wire_to_value(args[0], item) for item in data]

        if origin is dict:
            return {key: cls._wire_to_value(args[1], value) for key, value in data.items()}

        if origin is tuple:
            return tuple(cls._wire_to_value(arg, item) for arg, item in zip(args, data))

        if origin in (Union, UnionType):
            for arg in args:
                try:
                    return cls._wire_to_value(arg, data)
                except (TypeError, ValueError, KeyError, IndexError):
                    pass
            return data

        try:
            if issubclass(annotation, OCCIDModel):
                return annotation._from_wire(data)
        except TypeError:
            pass

        try:
            if issubclass(annotation, IntEnum):
                return annotation(data)
        except TypeError:
            pass

        try:
            if issubclass(annotation, Enum):
                return annotation(data)
        except TypeError:
            pass

        return data

    @classmethod
    def _wire_value(cls, value):
        if issubclass(type(value), OCCIDModel):
            values = [cls._wire_value(getattr(value, field_name)) for field_name in value.model_fields]
            while values and values[-1] is None:
                values.pop()
            return values
        if type(value) == dict:
            return {key: cls._wire_value(item) for key, item in value.items()}
        if type(value) in (list, tuple):
            return [cls._wire_value(item) for item in value]
        if issubclass(type(value), IntEnum):
            return value.value
        if issubclass(type(value), Enum):
            return value.value
        return value

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if type(value) == dict:
                return {key: encode(item) for key, item in value.items()}
            if type(value) in (list, tuple):
                return [encode(item) for item in value]
            if issubclass(type(value), IntEnum):
                return value.value
            if issubclass(type(value), Enum):
                return value.value
            return value

        if mode == "json":
            data = super().model_dump(mode="python", **kwargs)
            return encode(data)
        data = super().model_dump(mode=mode, **kwargs)
        return data
