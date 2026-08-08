"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

SchemaVersion = tuple[int, int, int]
OCCID_SCHEMA_VERSION: SchemaVersion = (4, 0, 0)

### Enums

class IntEnum(_StdIntEnum):
    @classmethod
    def _missing_(cls, value):
        if type(value) == str:
            return cls[value]
        return super()._missing_(value)

### Models

OCCID_MODEL_BY_ID = {}
OCCID_MODEL_ID_BY_CLASS = {}


class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __occid_model_id__: ClassVar[int | None] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        model_id = getattr(cls, "__occid_model_id__", None)
        if model_id is not None:
            OCCID_MODEL_BY_ID[model_id] = cls
            OCCID_MODEL_ID_BY_CLASS[cls] = model_id

    def encode(self) -> bytes:
        envelope = {
            "schema_version": list(OCCID_SCHEMA_VERSION),
            "model_id": OCCID_MODEL_ID_BY_CLASS[type(self)],
            "fields": self._wire_model_fields(self),
        }
        return msgpack.packb(envelope, use_bin_type=True)

    @classmethod
    def decode(cls, payload: bytes):
        envelope = msgpack.unpackb(payload, raw=False)
        version = tuple(envelope["schema_version"])
        if version != OCCID_SCHEMA_VERSION:
            raise ValueError(f"unsupported OCCID schema version {version}; expected {OCCID_SCHEMA_VERSION}")
        model_id = envelope["model_id"]
        if model_id != OCCID_MODEL_ID_BY_CLASS[cls]:
            raise ValueError(f"payload model ID {model_id} does not identify {cls.__name__}")
        return cls._from_wire_fields(envelope["fields"])

    @classmethod
    def _from_wire_fields(cls, data):
        values = {
            field_name: cls._wire_to_value(cls.model_fields[field_name].annotation, value)
            for field_name, value in data.items()
        }
        return cls(**values)

    @classmethod
    def _wire_to_value(cls, annotation, data):
        if data is None:
            return None

        origin = get_origin(annotation)
        args = get_args(annotation)

        if type(data) == dict and set(data) == {"model_id", "fields"}:
            return OCCID_MODEL_BY_ID[data["model_id"]]._from_wire_fields(data["fields"])

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
                return annotation._from_wire_fields(data)
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
            return {
                "model_id": OCCID_MODEL_ID_BY_CLASS[type(value)],
                "fields": cls._wire_model_fields(value),
            }
        if type(value) == dict:
            return {key: cls._wire_value(item) for key, item in value.items()}
        if type(value) in (list, tuple):
            return [cls._wire_value(item) for item in value]
        if issubclass(type(value), IntEnum):
            return value.value
        if issubclass(type(value), Enum):
            return value.value
        return value

    @classmethod
    def _wire_model_fields(cls, value):
        return {
            field_name: cls._wire_value(getattr(value, field_name))
            for field_name in type(value).model_fields
        }

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
