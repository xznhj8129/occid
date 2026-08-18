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
    'Identified physical-world spatial reference, place, feature, site, course, area, or delimiter'
    __occid_model_id__: ClassVar[int] = 22
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    location_id: StringID
    name: builtins.str | None = None

class Mark(Location):
    'Identified point reference in physical space'
    __occid_model_id__: ClassVar[int] = 328
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    position: GlobalPosition

class Path(Location):
    'Identified ordered spatial course or trace'
    __occid_model_id__: ClassVar[int] = 329
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    path: GeoPath

class Region(Location):
    'Identified bounded spatial area'
    __occid_model_id__: ClassVar[int] = 330
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    area: GeoArea

class Boundary(Location):
    'Identified spatial line that delimits, separates, or gates space'
    __occid_model_id__: ClassVar[int] = 331
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    path: GeoPath
