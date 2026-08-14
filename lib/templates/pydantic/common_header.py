"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
import re
import sys
from types import UnionType
from enum import IntEnum as _StdIntEnum, IntEnum, IntFlag, auto, Enum
from typing import Annotated, Any, ClassVar, Literal, Union, get_args, get_origin
import msgpack
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, model_validator

SchemaVersion = tuple[int, int, int]
OCCID_SCHEMA_VERSION: SchemaVersion = (5, 0, 0)
