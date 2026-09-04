"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Collection(OCCIDModel):
    'Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal'
    __occid_model_id__: ClassVar[int] = 32
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None

class Cluster(OCCIDModel):
    'A set of objects united only by criterion'
    __occid_model_id__: ClassVar[int] = 31
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None

class Equipment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 65
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None

class Component(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 36
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None

class Location(OCCIDModel):
    'Identified physical-world spatial reference, place, feature, site, course, area, or delimiter'
    __occid_model_id__: ClassVar[int] = 129
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Symbology | None = None

class Mark(OCCIDModel):
    'Identified point reference in physical space'
    __occid_model_id__: ClassVar[int] = 135
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Symbology | None = None
    position: GlobalPosition

class Path(OCCIDModel):
    'Identified ordered spatial course or trace'
    __occid_model_id__: ClassVar[int] = 177
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Symbology | None = None
    path: GeoPath

class Region(OCCIDModel):
    'Identified bounded spatial area'
    __occid_model_id__: ClassVar[int] = 204
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Symbology | None = None
    area: GeoArea

class Boundary(OCCIDModel):
    'Identified spatial line that delimits, separates, or gates space'
    __occid_model_id__: ClassVar[int] = 22
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Location')]
    name: builtins.str | None = None
    symbology: Symbology | None = None
    path: GeoPath
