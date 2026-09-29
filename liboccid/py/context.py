"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Context(OCCIDModel):
    'Semantic context that bounds the interpretation of operational objects without embedding those objects into one document aggregate'
    __occid_model_id__: ClassVar[int] = 55
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('OperationalContext',)

class OperationalContext(OCCIDModel):
    'Identified operational context with declared reality and temporal extent'
    __occid_model_id__: ClassVar[int] = 227
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Context'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Operation', 'Scenario')
    uid: Semantic[ID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[ID]]

class Operation(OCCIDModel):
    'Operational context describing an undertaking conducted by participating actors or organizations'
    __occid_model_id__: ClassVar[int] = 226
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OperationalContext'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[ID]]

class Scenario(OCCIDModel):
    'Operational context used to describe, rehearse, simulate, or replay a bounded situation'
    __occid_model_id__: ClassVar[int] = 288
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OperationalContext'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[ID]]
