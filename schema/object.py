"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Object(OCCIDModel):
    'Atoms'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Entity', 'Set', 'Item', 'Location')
    capabilities: list[Semantic[Capability]] | None = None

class Set(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 241
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Object'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Collection', 'Cluster', 'Organization')
    capabilities: list[Semantic[Capability]] | None = None

class Collection(OCCIDModel):
    'Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal'
    __occid_model_id__: ClassVar[int] = 34
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Set'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None

class Cluster(OCCIDModel):
    'A set of objects united only by criterion'
    __occid_model_id__: ClassVar[int] = 33
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Set'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None

class Item(OCCIDModel):
    'A discrete bounded non-agent object'
    __occid_model_id__: ClassVar[int] = 126
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Object'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Equipment', 'Component', 'Payload')
    capabilities: list[Semantic[Capability]] | None = None

class Equipment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 75
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Item'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None

class Component(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 40
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Item'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None

class Location(OCCIDModel):
    'Identified physical-world spatial reference, place, feature, site, course, area, or delimiter'
    __occid_model_id__: ClassVar[int] = 141
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Object'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Mark', 'Path', 'Region', 'Boundary')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Semantic[Symbology] | None = None

class Mark(OCCIDModel):
    'Identified point reference in physical space'
    __occid_model_id__: ClassVar[int] = 147
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Location'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Semantic[Symbology] | None = None
    position: Semantic[GlobalPosition]

class Path(OCCIDModel):
    'Identified ordered spatial course or trace'
    __occid_model_id__: ClassVar[int] = 193
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Location'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Semantic[Symbology] | None = None
    path: Semantic[GeoPath]

class Region(OCCIDModel):
    'Identified bounded spatial area'
    __occid_model_id__: ClassVar[int] = 220
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Location'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Semantic[Symbology] | None = None
    area: Semantic[GeoArea]

class Boundary(OCCIDModel):
    'Identified spatial line that delimits, separates, or gates space'
    __occid_model_id__: ClassVar[int] = 24
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Location'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Semantic[Symbology] | None = None
    path: Semantic[GeoPath]
