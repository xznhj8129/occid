"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Context(OCCIDModel):
    'Semantic context that bounds the interpretation of operational objects without embedding those objects into one document aggregate'
    __occid_model_id__: ClassVar[int] = 65
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('OperationalContext',)

class OperationalContext(OCCIDModel):
    'Identified operational context with declared reality and temporal extent'
    __occid_model_id__: ClassVar[int] = 261
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Context'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Operation', 'Scenario')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OperationalContext')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[UID]]

class Operation(OCCIDModel):
    'Operational context describing an undertaking conducted by participating actors or organizations'
    __occid_model_id__: ClassVar[int] = 260
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OperationalContext'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OperationalContext')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[UID]]

class Scenario(OCCIDModel):
    'Operational context used to describe, rehearse, simulate, or replay a bounded situation'
    __occid_model_id__: ClassVar[int] = 332
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OperationalContext'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OperationalContext')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    reality: Reality
    temporal_extent: Semantic[TimeRange] | None = None
    member_uids: list[Semantic[UID]]
