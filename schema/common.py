"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from importlib.metadata import PackageNotFoundError as _PackageNotFoundError, version as _distribution_version
from pathlib import Path as _Path
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Generic, Literal, TypeVar, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, RootModel


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

from pydantic_core import core_schema


### Models

OCCID_MODEL_BY_ID = {}
OCCID_MODEL_ID_BY_CLASS = {}
OCCID_MODEL_BY_NAME = {}
OCCID_PARENT_BY_NAME = {}
OCCID_CHILDREN_BY_NAME = {}
_OCCIDValueT = TypeVar("_OCCIDValueT")


class IDNamespace(str):
    """Schema-defined namespace attached to an IntID type expression."""


def _occid_model_name(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, type):
        return value.__name__
    return type(value).__name__


def is_a(actual, expected) -> bool:
    """Return whether ``actual`` is ``expected`` or a semantic descendant.

    Semantic ancestry is the compiled OCCID parent graph. Python inheritance is
    deliberately irrelevant: generated runtime classes remain flat.
    """
    current = _occid_model_name(actual)
    target = _occid_model_name(expected)
    if current not in OCCID_PARENT_BY_NAME or target not in OCCID_PARENT_BY_NAME:
        return False

    seen = set()
    while current is not None:
        if current == target:
            return True
        if current in seen:
            raise RuntimeError(f"OCCID semantic parent cycle involving {current}")
        seen.add(current)
        current = OCCID_PARENT_BY_NAME.get(current)
    return False


def children_of(model) -> tuple[str, ...]:
    """Return direct semantic children derived by the compiler from ``parent``."""
    return OCCID_CHILDREN_BY_NAME.get(_occid_model_name(model), ())


class SemanticReference:
    """Pydantic metadata for one nominal OCCID semantic reference.

    JSON/dict validation keeps the declared model's stable schema. Python values
    may additionally be any already-materialized flat OCCID model satisfying the
    semantic parent graph. Compact-wire decoding uses the concrete model ID and
    performs the same semantic check before constructing the nested value.
    """

    def __init__(self, expected: str):
        self.expected = expected

    def __repr__(self) -> str:
        return f"SemanticReference({self.expected!r})"

    def __get_pydantic_core_schema__(self, source_type, handler):
        base_schema = handler(source_type)

        def validate(value):
            if not isinstance(value, (OCCIDModel, OCCIDValue)) or not is_a(value, self.expected):
                actual = _occid_model_name(value)
                raise ValueError(f"{actual} is not semantically compatible with {self.expected}")
            return value

        def serialize(value, info):
            return value.model_dump(mode=info.mode, serialize_as_any=True)

        python_schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(OCCIDModel),
                core_schema.is_instance_schema(OCCIDValue),
                base_schema,
            ],
            mode="left_to_right",
        )
        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.json_or_python_schema(
                json_schema=base_schema,
                python_schema=python_schema,
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                info_arg=True,
            ),
        )


class Semantic:
    """Stable runtime annotation for a nominal OCCID semantic model reference."""

    def __class_getitem__(cls, expected):
        if not isinstance(expected, type):
            raise TypeError("Semantic[...] expects an OCCID model class")
        return Annotated[expected, SemanticReference(expected.__name__)]


def _register_occid_model(cls) -> None:
    model_id = getattr(cls, "__occid_model_id__", None)
    if model_id is None:
        return
    name = cls.__name__
    OCCID_MODEL_BY_ID[model_id] = cls
    OCCID_MODEL_ID_BY_CLASS[cls] = model_id
    OCCID_MODEL_BY_NAME[name] = cls
    OCCID_PARENT_BY_NAME[name] = getattr(cls, "__occid_parent__", None)
    OCCID_CHILDREN_BY_NAME[name] = tuple(getattr(cls, "__occid_children__", ()))


def _validate_semantic_registry() -> None:
    """Assert that compiled children are exactly the reverse parent index."""
    expected = {name: [] for name in OCCID_PARENT_BY_NAME}
    for child, parent in OCCID_PARENT_BY_NAME.items():
        if parent is None:
            continue
        if parent not in expected:
            raise RuntimeError(f"unknown OCCID semantic parent {parent!r} for {child}")
        expected[parent].append(child)

    for parent, children in expected.items():
        actual = list(OCCID_CHILDREN_BY_NAME.get(parent, ()))
        if set(actual) != set(children):
            raise RuntimeError(
                f"compiled OCCID children disagree with parent edges for {parent}: "
                f"expected {children}, got {actual}"
            )


def _semantic_reference(metadata) -> SemanticReference | None:
    for item in metadata or ():
        if isinstance(item, SemanticReference):
            return item
    return None


class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __occid_model_id__: ClassVar[int | None] = None
    __occid_semantic_role__: ClassVar[str | None] = None
    __occid_parent__: ClassVar[str | None] = None
    __occid_children__: ClassVar[tuple[str, ...]] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__occid_semantic_role__" not in cls.__dict__:
            cls.__occid_semantic_role__ = None
        _register_occid_model(cls)

    def encode(self) -> bytes:
        """Encode one OCCID model into the compact binary wire form.

        Wire shape: [model_id, {field_ordinal: value, ...}]. Field names and
        model names never appear on the compact wire. Atomic values use their
        declared underlying representation when the concrete model is exactly
        the field's declared semantic model.
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
            field_info = cls.model_fields[field_name]
            values[field_name] = cls._wire_to_value(
                field_info.annotation,
                raw_value,
                field_info.metadata,
            )
        return cls(**values)

    @classmethod
    def _wire_to_semantic(cls, expected: str, data):
        if type(data) is list and len(data) == 2 and type(data[0]) is int:
            model_id, model_payload = data
            model_cls = OCCID_MODEL_BY_ID.get(model_id)
            if model_cls is None:
                raise ValueError(f"unknown OCCID model ID {model_id}")
            if not is_a(model_cls, expected):
                raise ValueError(
                    f"model ID {model_id} ({model_cls.__name__}) is not semantically compatible with {expected}"
                )
            if issubclass(model_cls, OCCIDValue):
                return model_cls._from_wire_value(model_payload)
            return model_cls._from_wire_fields(model_payload)

        expected_cls = OCCID_MODEL_BY_NAME.get(expected)
        if expected_cls is None:
            raise ValueError(f"unknown OCCID semantic model {expected}")
        if issubclass(expected_cls, OCCIDValue):
            return expected_cls._from_wire_value(data)
        raise ValueError(f"nested semantic {expected} model must be [model_id, fields]")

    @classmethod
    def _wire_to_value(cls, annotation, data, metadata=()):
        if data is None:
            return None

        semantic = _semantic_reference(metadata)
        if semantic is not None:
            return cls._wire_to_semantic(semantic.expected, data)

        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is Annotated:
            return cls._wire_to_value(args[0], data, args[1:])

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
                    if model_cls is not annotation:
                        raise ValueError(
                            f"model ID {model_id} does not identify {annotation.__name__}"
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
                if model_cls is not annotation:
                    raise ValueError(
                        f"model ID {model_id} does not identify {annotation.__name__}"
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
    def _wire_value(cls, value, annotation=None, metadata=()):
        semantic = _semantic_reference(metadata)
        if semantic is not None:
            if not is_a(value, semantic.expected):
                raise ValueError(
                    f"{_occid_model_name(value)} is not semantically compatible with {semantic.expected}"
                )
            if isinstance(value, OCCIDValue):
                root_annotation = type(value).model_fields["root"].annotation
                if type(value).__name__ == semantic.expected:
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

        origin = get_origin(annotation)
        args = get_args(annotation)
        if origin is Annotated:
            return cls._wire_value(value, args[0], args[1:])

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
        """Encode explicitly present fields by numeric ordinal."""
        result = {}
        for field_id, field_name in enumerate(type(value).model_fields):
            if field_name not in value.model_fields_set:
                continue
            field_info = type(value).model_fields[field_name]
            result[field_id] = cls._wire_value(
                getattr(value, field_name),
                field_info.annotation,
                field_info.metadata,
            )
        return result


class OCCIDValue(RootModel[_OCCIDValueT], Generic[_OCCIDValueT]):
    """Named atomic OCCID representation with one direct typed value."""

    __occid_model_id__: ClassVar[int | None] = None
    __occid_semantic_role__: ClassVar[str | None] = None
    __occid_parent__: ClassVar[str | None] = None
    __occid_children__: ClassVar[tuple[str, ...]] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__occid_semantic_role__" not in cls.__dict__:
            cls.__occid_semantic_role__ = None
        _register_occid_model(cls)

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
        field_info = cls.model_fields["root"]
        value = OCCIDModel._wire_to_value(field_info.annotation, data, field_info.metadata)
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
