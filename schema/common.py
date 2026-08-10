"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

SchemaVersion = tuple[int, int, int]
OCCID_SCHEMA_VERSION: SchemaVersion = (4, 1, 0)

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
        model = decode_model(payload)
        if type(model) is not cls:
            model_id = OCCID_MODEL_ID_BY_CLASS[type(model)]
            raise ValueError(f"payload model ID {model_id} does not identify {cls.__name__}")
        return model

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

        if origin in (Union, UnionType):
            for option in args:
                if option is type(None):
                    continue
                try:
                    return cls._wire_to_value(option, data)
                except Exception:
                    continue
            return data

        if origin is Annotated and args:
            return cls._wire_to_value(args[0], data)

        if origin is list:
            item_type = args[0] if args else Any
            return [cls._wire_to_value(item_type, value) for value in data]

        if origin is dict:
            value_type = args[1] if len(args) > 1 else Any
            return {key: cls._wire_to_value(value_type, value) for key, value in data.items()}

        if origin is Literal:
            return data

        if isinstance(annotation, type) and issubclass(annotation, OCCIDModel):
            if not isinstance(data, dict) or "model_id" not in data or "fields" not in data:
                return annotation.model_validate(data)
            model_id = data["model_id"]
            model_type = OCCID_MODEL_BY_ID.get(model_id)
            if model_type is None:
                raise ValueError(f"unknown OCCID model ID {model_id}")
            if not issubclass(model_type, annotation):
                raise ValueError(
                    f"model ID {model_id} identifies {model_type.__name__}, "
                    f"not a {annotation.__name__}"
                )
            return model_type._from_wire_fields(data["fields"])

        if isinstance(annotation, type) and issubclass(annotation, Enum):
            return annotation(data)

        return data

    @classmethod
    def _wire_value(cls, value):
        if isinstance(value, OCCIDModel):
            return {
                "model_id": OCCID_MODEL_ID_BY_CLASS[type(value)],
                "fields": cls._wire_model_fields(value),
            }
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, dict):
            return {key: cls._wire_value(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls._wire_value(item) for item in value]
        return value

    @classmethod
    def _wire_model_fields(cls, model):
        return {
            name: cls._wire_value(getattr(model, name))
            for name in model.__class__.model_fields
        }

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if isinstance(value, Enum):
                return value.name
            if isinstance(value, OCCIDModel):
                return {
                    name: encode(getattr(value, name))
                    for name in value.__class__.model_fields
                }
            if isinstance(value, dict):
                return {key: encode(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [encode(item) for item in value]
            return value

        if mode == "json":
            return {
                name: encode(getattr(self, name))
                for name in self.__class__.model_fields
                if not kwargs.get("exclude_none") or getattr(self, name) is not None
            }
        return super().model_dump(mode=mode, **kwargs)


def decode_model(payload: bytes):
    envelope = msgpack.unpackb(payload, raw=False)
    schema_version = tuple(envelope["schema_version"])
    if schema_version != OCCID_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported OCCID schema version {schema_version}; "
            f"expected {OCCID_SCHEMA_VERSION}"
        )
    model_id = envelope["model_id"]
    model_type = OCCID_MODEL_BY_ID.get(model_id)
    if model_type is None:
        raise ValueError(f"unknown OCCID model ID {model_id}")
    return model_type._from_wire_fields(envelope["fields"])
