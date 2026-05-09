"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class ObjectType(IntEnum):
    ENTITY = 0
    ORGANIZATION = auto()

### Models

class BaseObject(SigmaModel):
    object_type: ObjectType
