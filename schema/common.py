"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from importlib.metadata import PackageNotFoundError as _PackageNotFoundError, version as _distribution_version
from pathlib import Path as _Path
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Generic, Literal, TypeVar, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, RootModel, SerializeAsAny


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
_OCCIDValueT = TypeVar("_OCCIDValueT")


class IDNamespace(str):
    """Schema-defined namespace attached to an IntID type expression."""


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
        model names never appear on the compact wire. Atomic values use their
        declared underlying representation when the field type is exact.
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
            if type(data) is list and len(data) == 2 and type(data[0]) is int:
                model_cls = OCCID_MODEL_BY_ID.get(data[0])
                if model_cls is not None and issubclass(model_cls, OCCIDValue):
                    for arg in args:
                        try:
                            if arg is not type(None) and issubclass(model_cls, arg):
                                return model_cls._from_wire_value(data[1])
                        except TypeError:
                            continue
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
            if issubclass(annotation, OCCIDValue):
                if type(data) is list and len(data) == 2 and type(data[0]) is int:
                    model_id, raw_value = data
                    model_cls = OCCID_MODEL_BY_ID.get(model_id)
                    if model_cls is None:
                        raise ValueError(f"unknown OCCID model ID {model_id}")
                    if not issubclass(model_cls, annotation):
                        raise ValueError(
                            f"model ID {model_id} is not compatible with {annotation.__name__}"
                        )
                    return model_cls._from_wire_value(raw_value)
                return annotation._from_wire_value(data)
        except TypeError:
            pass

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
    def _wire_value(cls, value, annotation=None):
        origin = get_origin(annotation)
        args = get_args(annotation)
        if origin is Annotated:
            annotation = args[0]
            origin = get_origin(annotation)
            args = get_args(annotation)

        if isinstance(value, OCCIDValue):
            root_annotation = type(value).model_fields["root"].annotation
            if annotation is type(value):
                return cls._wire_value(value.root, root_annotation)
            return [
                OCCID_MODEL_ID_BY_CLASS[type(value)],
                cls._wire_value(value.root, root_annotation),
            ]
        if isinstance(value, OCCIDModel):
            return [
                OCCID_MODEL_ID_BY_CLASS[type(value)],
                cls._wire_model_fields(value),
            ]
        if type(value) is dict:
            value_annotation = args[1] if origin is dict and len(args) == 2 else None
            return {
                key: cls._wire_value(item, value_annotation)
                for key, item in value.items()
            }
        if type(value) in (list, tuple):
            if origin is list and args:
                return [cls._wire_value(item, args[0]) for item in value]
            if origin is tuple and args and len(args) == len(value):
                return [cls._wire_value(item, arg) for item, arg in zip(value, args)]
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
            field_id: cls._wire_value(
                getattr(value, field_name),
                type(value).model_fields[field_name].annotation,
            )
            for field_id, field_name in enumerate(type(value).model_fields)
            if field_name in value.model_fields_set
        }


class OCCIDValue(RootModel[_OCCIDValueT], Generic[_OCCIDValueT]):
    """Named atomic OCCID representation with one direct typed value."""

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
        root_annotation = type(self).model_fields["root"].annotation
        envelope = [
            OCCID_MODEL_ID_BY_CLASS[type(self)],
            OCCIDModel._wire_value(self.root, root_annotation),
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
    def _from_wire_value(cls, data):
        annotation = cls.model_fields["root"].annotation
        value = OCCIDModel._wire_to_value(annotation, data)
        return cls(root=value)


def decode_model(payload: bytes) -> OCCIDModel | OCCIDValue:
    """Decode a heterogeneous OCCID compact binary envelope."""
    envelope = msgpack.unpackb(
        payload,
        raw=False,
        strict_map_key=False,
    )
    if type(envelope) is not list or len(envelope) != 2:
        raise ValueError("OCCID payload must be [model_id, payload]")

    model_id, model_payload = envelope
    if type(model_id) is not int:
        raise ValueError("OCCID model ID must be an integer")

    model_cls = OCCID_MODEL_BY_ID.get(model_id)
    if model_cls is None:
        raise ValueError(f"unknown OCCID model ID {model_id}")
    if issubclass(model_cls, OCCIDValue):
        return model_cls._from_wire_value(model_payload)
    return model_cls._from_wire_fields(model_payload)
