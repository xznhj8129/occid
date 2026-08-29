"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from importlib.metadata import PackageNotFoundError as _PackageNotFoundError, version as _distribution_version
from pathlib import Path as _Path
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, StringConstraints

OCCIDID = Annotated[
    builtins.str,
    StringConstraints(
        strict=True,
        to_lower=True,
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
    ),
]

OCCIDVersion = tuple[int, int, int]
try:
    _version_text = _distribution_version("occid")
except _PackageNotFoundError:
    _version_text = (_Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()
_version_parts = tuple(int(part) for part in _version_text.split("."))
if len(_version_parts) != 3:
    raise RuntimeError(f"invalid OCCID VERSION {_version_text!r}")
OCCID_VERSION: OCCIDVersion = _version_parts
