"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .information import Information

### Enums

class Properties_type(IntEnum):
    IDENTITY = 0
    ATTRIBUTES = auto()
    PARAMETERS = auto()
    RELATIONSHIP = auto()

### Models

class Properties(Information):
    'A generally fixed characteristic, classification, disposition, or capability that defines an object, but is not merely its momentary condition'

class FeaturePropertyValue(Properties):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class FeatureProperty(Properties):
    key: str
    value: FeaturePropertyValue
