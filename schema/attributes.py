"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .properties import Attributes

### Enums

class ClassificationLevel(IntEnum):
    UNCLASSIFIED = 0
    CONTROLLED = auto()
    CONFIDENTIAL = auto()
    SECRET = auto()
    TOP_SECRET = auto()

### Models

class MetadataValue(Attributes):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class MetadataEntry(Attributes):
    key: str
    value: MetadataValue

class SymbologySchema(Attributes):
    sidc: str | None = None
    cot: str | None = None

class DisplayMeta(Attributes):
    icon_code: str | None = None
    tint: str | None = None
    short_label: str | None = None

class ClassificationSchema(Attributes):
    level: ClassificationLevel
    codewords: list[str]
    release_to: list[str]

class SensorFieldOfView(Attributes):
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None

class Version(Attributes):
    major: int
    minor: int
    patch: int
