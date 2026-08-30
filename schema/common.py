"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from importlib.metadata import PackageNotFoundError as _PackageNotFoundError, version as _distribution_version
from pathlib import Path as _Path
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
from uuid import SafeUUID, UUID
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny
from pydantic_core import core_schema


class UID(UUID):
    """Canonical OCCID identity.

    UUIDv4 is the identity-v1 allocation scheme. UUID text is a human/API
    representation only; compact OCCID serialization carries the 128-bit value
    as exactly 16 payload bytes.
    """

    def __init__(
        self,
        hex=None,
        bytes=None,
        bytes_le=None,
        fields=None,
        int=None,
        version=None,
        *,
        is_safe=SafeUUID.unknown,
    ):
        super().__init__(
            hex=hex,
            bytes=bytes,
            bytes_le=bytes_le,
            fields=fields,
            int=int,
            version=version,
            is_safe=is_safe,
        )
        if self.version != 4:
            raise ValueError("UID must be UUIDv4")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        def cast(value):
            if isinstance(value, cls):
                return value
            return cls(str(value))

        return core_schema.no_info_after_validator_function(
            cast,
            core_schema.uuid_schema(version=4),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                when_used="json",
            ),
        )


OCCIDVersion = tuple[int, int, int]
try:
    _version_text = _distribution_version("occid")
except _PackageNotFoundError:
    _version_text = (_Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
_version_parts = tuple(int(part) for part in _version_text.split("."))
if len(_version_parts) != 3:
    raise RuntimeError(f"invalid OCCID VERSION {_version_text!r}")
OCCID_VERSION: OCCIDVersion = _version_parts

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
    __occid_semantic_role__: ClassVar[str | None] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__occid_semantic_role__" not in cls.__dict__:
            cls.__occid_semantic_role__ = None
        model_id = getattr(cls, "__occid_model_id__", None)
        if model_id is not None:
            OCCID_MODEL_BY_ID[model_id] = cls
            OCCID_MODEL_ID_BY_CLASS[cls] = model_id

    def encode(self) -> bytes:
        """Encode one OCCID model into the compact binary wire form.

        Wire shape: [model_id, {field_ordinal: value, ...}]. Field names and
        model names never appear on the compact wire. UID values are bin16.
        """
        envelope = [
            OCCID_MODEL_ID_BY_CLASS[type(self)],
            self._wire_model_fields(self),
        ]
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
        if type(data) is not dict:
            raise ValueError("OCCID wire fields must be a numeric map")

        field_names = tuple(cls.model_fields)
        values = {}
        for field_id, raw_value in data.items():
            if type(field_id) is not int or field_id < 0 or field_id >= len(field_names):
                raise ValueError(f"invalid field ordinal {field_id!r} for {cls.__name__}")
            field_name = field_names[field_id]
            values[field_name] = cls._wire_to_value(
                cls.model_fields[field_name].annotation,
                raw_value,
            )
        return cls(**values)

    @classmethod
    def _wire_to_value(cls, annotation, data):
        if data is None:
            return None

        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is Annotated:
            return cls._wire_to_value(args[0], data)

        if origin in (Union, UnionType):
            last_error = None
            for arg in args:
                if arg is type(None):
                    continue
                try:
                    return cls._wire_to_value(arg, data)
                except (TypeError, ValueError, KeyError, IndexError) as exc:
                    last_error = exc
            if last_error is not None:
                raise last_error
            return data

        if annotation is UID:
            if type(data) is not bytes or len(data) != 16:
                raise ValueError("UID wire value must be exactly 16 bytes")
            return UID(bytes=data)

        if origin is list:
            return [cls._wire_to_value(args[0], item) for item in data]

        if origin is dict:
            return {
                key: cls._wire_to_value(args[1], value)
                for key, value in data.items()
            }

        if origin is tuple:
            if len(data) != len(args):
                raise ValueError("tuple wire value has incorrect length")
            return tuple(
                cls._wire_to_value(arg, item)
                for arg, item in zip(args, data)
            )

        try:
            if issubclass(annotation, OCCIDModel):
                if type(data) is not list or len(data) != 2:
                    raise ValueError("nested OCCID model must be [model_id, fields]")
                model_id, fields = data
                model_cls = OCCID_MODEL_BY_ID.get(model_id)
                if model_cls is None:
                    raise ValueError(f"unknown OCCID model ID {model_id}")
                if not issubclass(model_cls, annotation):
                    raise ValueError(
                        f"model ID {model_id} is not compatible with {annotation.__name__}"
                    )
                return model_cls._from_wire_fields(fields)
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
        if isinstance(value, OCCIDModel):
            return [
                OCCID_MODEL_ID_BY_CLASS[type(value)],
                cls._wire_model_fields(value),
            ]
        if isinstance(value, UID):
            return value.bytes
        if type(value) is dict:
            return {
                key: cls._wire_value(item)
                for key, item in value.items()
            }
        if type(value) in (list, tuple):
            return [cls._wire_value(item) for item in value]
        if isinstance(value, IntEnum):
            return value.value
        if isinstance(value, Enum):
            return value.value
        return value

    @classmethod
    def _wire_model_fields(cls, value):
        """Encode explicitly present fields by numeric ordinal.

        The ordinal is the field's index in the effective generated model field
        order for this OCCID contract. Optional/default fields not explicitly
        present are omitted. Peers are expected to share the same OCCID contract.
        """
        return {
            field_id: cls._wire_value(getattr(value, field_name))
            for field_id, field_name in enumerate(type(value).model_fields)
            if field_name in value.model_fields_set
        }


def decode_model(payload: bytes) -> OCCIDModel:
    """Decode a heterogeneous OCCID compact binary envelope."""
    envelope = msgpack.unpackb(
        payload,
        raw=False,
        strict_map_key=False,
    )
    if type(envelope) is not list or len(envelope) != 2:
        raise ValueError("OCCID payload must be [model_id, fields]")

    model_id, fields = envelope
    if type(model_id) is not int:
        raise ValueError("OCCID model ID must be an integer")

    model_cls = OCCID_MODEL_BY_ID.get(model_id)
    if model_cls is None:
        raise ValueError(f"unknown OCCID model ID {model_id}")
    return model_cls._from_wire_fields(fields)
