"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from pathlib import Path
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

SchemaVersion = tuple[int, int, int]
_version_text = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
_version_parts = tuple(int(part) for part in _version_text.split("."))
if len(_version_parts) != 3:
    raise RuntimeError(f"invalid OCCID VERSION {_version_text!r}")
OCCID_SCHEMA_VERSION: SchemaVersion = _version_parts
