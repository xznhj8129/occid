"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class RelationshipKind(IntEnum):
    MEMBER_OF = 0
    COMMANDS = auto()
    OPERATES = auto()
    SUPPORTS = auto()
    OWNS = auto()

class SpatialRelationKind(IntEnum):
    CONTAINS = 0
    WITHIN = auto()
    INTERSECTS = auto()
    OVERLAPS = auto()
    TOUCHES = auto()
    CROSSES = auto()
    CONNECTS = auto()

### Models

class Relationship(OCCIDModel):
    'Nature of relations, ownership, provenance, link'
    __occid_model_id__: ClassVar[int] = 220
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DirectedRelationship', 'EntityComponentRef', 'SpatialRelationship')

class DirectedRelationship(OCCIDModel):
    'Typed directed semantic relationship between two OCCID objects'
    __occid_model_id__: ClassVar[int] = 61
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Relationship'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[UID]
    object_uid: Semantic[UID]
    relation: RelationshipKind
    since_ts: Semantic[Timestamp] | None = None
    until_ts: Semantic[Timestamp] | None = None
    confidence: ConfidenceLevel | None = None
    source: builtins.str | None = None

class EntityComponentRef(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 72
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Relationship'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    component_ref: builtins.str
    component_type: builtins.str | None = None
    label: builtins.str | None = None

class SpatialRelationship(OCCIDModel):
    'Persisted asserted topological relationship between identified spatial objects; subject is related to reference by relation'
    __occid_model_id__: ClassVar[int] = 242
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Relationship'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Relationship')]
    subject_uid: Semantic[UID]
    reference_uid: Semantic[UID]
    relation: SpatialRelationKind
