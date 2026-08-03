"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Relationship(Property):
    'Nature of relations, ownership, provenance, link'
    __occid_model_id__: ClassVar[int] = 181

class RelationSchema(Relationship):
    __occid_model_id__: ClassVar[int] = 182
    src_id: StringID
    dst_id: StringID
    rel_kind: builtins.str
    since_ts: builtins.float | None = None
    until_ts: builtins.float | None = None
    confidence: ConfidenceLevel | None = None
    source: builtins.str | None = None

class EntityComponentRef(Relationship):
    __occid_model_id__: ClassVar[int] = 183
    component_id: StringID
    component_type: builtins.str | None = None
    label: builtins.str | None = None
