"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Enums

class Object_type(IntEnum):
    ENTITY = 0
    SET = auto()
    ITEM = auto()
    LOCATION = auto()

class Set_type(IntEnum):
    ORGANIZATION = 0
    COLLECTION = auto()
    CLUSTER = auto()

class Item_type(IntEnum):
    EQUIPMENT = 0
    COMPONENT = auto()
    PAYLOAD = auto()

### Models

class Object(Root):
    'Atoms'

class Set(Object):
    pass

class Collection(Set):
    'Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal'

class Cluster(Set):
    'A set of objects united only by criterion'

class Item(Object):
    'A discrete bounded non-agent object'

class Equipment(Item):
    pass

class Component(Item):
    pass

class Location(Object):
    'Physical-world feature, named location, site, or bounded place.'

class GeoJsonFeature(Location):
    id: StringID
    type: Literal['Feature'] = Field(default='Feature', frozen=True)
    geometry: GeoJsonGeometry
    properties: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(Collection):
    features: list[GeoJsonFeature]
    bbox: BoundingBox | None = None
