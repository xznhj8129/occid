"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Models

class Object(Root):
    'Atoms'
    __occid_model_id__: ClassVar[int] = 15
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    capabilities: list[Capability] | None = None

class Set(Object):
    __occid_model_id__: ClassVar[int] = 16
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Collection(Set):
    'Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal'
    __occid_model_id__: ClassVar[int] = 17
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Cluster(Set):
    'A set of objects united only by criterion'
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Item(Object):
    'A discrete bounded non-agent object'
    __occid_model_id__: ClassVar[int] = 19
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Equipment(Item):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Component(Item):
    __occid_model_id__: ClassVar[int] = 21
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Location(Object):
    'Physical-world feature, named location, site, or bounded place.'
    __occid_model_id__: ClassVar[int] = 22
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class GeoJsonFeature(Location):
    __occid_model_id__: ClassVar[int] = 23
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    id: StringID
    type: Literal['Feature'] = Field(default='Feature', frozen=True)
    geometry: GeoJsonGeometry
    properties: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(Collection):
    __occid_model_id__: ClassVar[int] = 24
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    features: list[GeoJsonFeature]
    bbox: BoundingBox | None = None

class MissionPoi(Location):
    'Named operational point of interest with stable identity and a concrete global position'
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    uid: StringID
    name: builtins.str
    pos: GlobalPosition
    origin: builtins.str
    cot: builtins.str | None = None
    added_ts: builtins.float | None = None
    stale_after_s: builtins.float | None = None
    url: builtins.str | None = None
