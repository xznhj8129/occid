"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class ObjectType(IntEnum):
    ENTITY = 0
    ORGANIZATION = auto()

class BaseObjectType(IntEnum):
    ENTITY = 0
    SET = auto()
    ITEM = auto()
    WORLD = auto()

class SetType(IntEnum):
    ORGANIZATION = 0
    COLLECTION = auto()
    CLUSTER = auto()
    SYSTEM = auto()

class OrganizationType(IntEnum):
    ORG = 0

class ItemType(IntEnum):
    RECORD = 0
    EQUIPMENT = auto()
    COMPONENT = auto()
    PAYLOAD = auto()

class WorldType(IntEnum):
    FEATURE = 0
    LOCATION = auto()
    SITE = auto()

### Models

class Object(Root):
    pass

class BaseObject(Object):
    object_type: ObjectType

class Entity(BaseObject):
    pass

class Set(BaseObject):
    pass

class Organization(Set):
    pass

class Collection(Set):
    pass

class Cluster(Set):
    pass

class System(Set):
    pass

class Item(BaseObject):
    pass

class Record(Item):
    pass

class Equipment(Item):
    pass

class Component(Item):
    pass

class Payload(Item):
    pass

class World(BaseObject):
    pass

class Feature(World):
    pass

class Location(World):
    pass

class Site(World):
    pass
