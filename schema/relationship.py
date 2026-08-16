"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Relationship(Property):
    'Nature of relations, ownership, provenance, link'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class RelationSchema(Relationship):
    __occid_model_id__: ClassVar[int] = 182
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    src_id: StringID
    dst_id: StringID
    rel_kind: builtins.str
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
