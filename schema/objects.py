"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class ObjectType(IntEnum):
    ENTITY = 0
    ORGANIZATION = auto()

class BaseObjectType(IntEnum):
    ENTITY = 0
    ORG = auto()

### Models

class BaseObject(OCCIDModel):
    object_type: ObjectType
