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
    __occid_model_id__: ClassVar[int] = 207
    __occid_semantic_role__: ClassVar[str] = 'type'

class DirectedRelationship(OCCIDModel):
    'Typed directed semantic relationship between two OCCID objects'
    __occid_model_id__: ClassVar[int] = 53
    __occid_semantic_role__: ClassVar[str] = 'representation'
    subject_uid: UID
    object_uid: UID
    relation: RelationshipKind
    since_ts: builtins.float | None = None
    until_ts: builtins.float | None = None
    confidence: ConfidenceLevel | None = None
    source: builtins.str | None = None

class EntityComponentRef(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 61
    __occid_semantic_role__: ClassVar[str] = 'representation'
    component_ref: builtins.str
    component_type: builtins.str | None = None
    label: builtins.str | None = None

class SpatialRelationship(OCCIDModel):
    'Persisted asserted topological relationship between identified spatial objects; subject is related to reference by relation'
    __occid_model_id__: ClassVar[int] = 227
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Relationship')]
    subject_uid: UID
    reference_uid: UID
    relation: SpatialRelationKind
