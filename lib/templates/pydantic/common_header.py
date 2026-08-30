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
