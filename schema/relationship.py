"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .properties import PropertyRelationship

### Models

class RelationSchema(PropertyRelationship):
    src_id: str
    dst_id: str
    rel_kind: str
    since_ts: float | None = None
    until_ts: float | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None

class EntityComponentRef(PropertyRelationship):
    component_id: str
    component_type: str | None = None
    label: str | None = None
