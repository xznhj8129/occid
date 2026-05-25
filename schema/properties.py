"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .information import Information

### Enums

class PropertiesType(IntEnum):
    IDENTITY = 0
    ATTRIBUTES = auto()
    PARAMETERS = auto()
    PROPERTY_RELATIONSHIP = auto()

### Models

class Properties(Information):
    pass

class Identity(Properties):
    pass

class Attributes(Properties):
    pass

class Parameters(Properties):
    pass

class PropertyRelationship(Properties):
    pass

class FeaturePropertyValue(Properties):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class FeatureProperty(Properties):
    key: str
    value: FeaturePropertyValue
