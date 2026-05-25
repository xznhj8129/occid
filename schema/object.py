"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class ObjectType(IntEnum):
    ENTITY = 0
    ORGANIZATION = auto()

class Object_type(IntEnum):
    ENTITY = 0
    SET = auto()
    ITEM = auto()
    WORLD = auto()

class Set_type(IntEnum):
    ORGANIZATION = 0
    COLLECTION = auto()
    CLUSTER = auto()
    SYSTEM = auto()

### Models

class Object(Root):
    object_type: ObjectType

class Set(Object):
    pass

class Collection(Set):
    pass

class Cluster(Set):
    pass

class System(Set):
    pass
