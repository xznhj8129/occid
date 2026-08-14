"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Models

class Object(Root):
    'Atoms'
    __occid_model_id__: ClassVar[int] = 15

class Set(Object):
    __occid_model_id__: ClassVar[int] = 16

class Collection(Set):
    'Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal'
    __occid_model_id__: ClassVar[int] = 17

class Cluster(Set):
    'A set of objects united only by criterion'
    __occid_model_id__: ClassVar[int] = 18

class Item(Object):
    'A discrete bounded non-agent object'
    __occid_model_id__: ClassVar[int] = 19

class Equipment(Item):
    __occid_model_id__: ClassVar[int] = 20

class Component(Item):
    __occid_model_id__: ClassVar[int] = 21

class Location(Object):
    'Physical-world feature, named location, site, or bounded place.'
    __occid_model_id__: ClassVar[int] = 22

class GeoJsonFeature(Location):
    __occid_model_id__: ClassVar[int] = 23
    id: StringID
    type: Literal['Feature'] = Field(default='Feature', frozen=True)
    geometry: GeoJsonGeometry
    properties: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(Collection):
    __occid_model_id__: ClassVar[int] = 24
    features: list[GeoJsonFeature]
    bbox: BoundingBox | None = None

class MissionPoi(Location):
    'Named operational point of interest with stable identity and a concrete global position'
    __occid_model_id__: ClassVar[int] = 117
    uid: StringID
    name: builtins.str
    pos: GlobalPosition
    origin: builtins.str
    cot: builtins.str | None = None
    added_ts: builtins.float | None = None
    stale_after_s: builtins.float | None = None
    url: builtins.str | None = None
