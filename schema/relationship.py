"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

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

class Relationship(Property):
    'Nature of relations, ownership, provenance, link'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class DirectedRelationship(Relationship):
    'Typed directed semantic relationship between two OCCID objects'
    __occid_model_id__: ClassVar[int] = 182
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    subject_uid: UID
    object_uid: UID
    relation: RelationshipKind
    since_ts: builtins.float | None = None
    until_ts: builtins.float | None = None
    confidence: ConfidenceLevel | None = None
    source: builtins.str | None = None

class EntityComponentRef(Relationship):
    __occid_model_id__: ClassVar[int] = 183
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    component_id: StringID
    component_type: builtins.str | None = None
    label: builtins.str | None = None

class SpatialRelationship(Relationship):
    'Persisted asserted topological relationship between identified spatial objects; subject is related to reference by relation'
    __occid_model_id__: ClassVar[int] = 332
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    uid: UID
    id: builtins.int
    subject_uid: UID
    reference_uid: UID
    relation: SpatialRelationKind
