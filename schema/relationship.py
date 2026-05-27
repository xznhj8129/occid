"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .properties import Properties

### Models

class Relationship(Properties):
    'Nature of relations, ownership, provenance, link'

class RelationSchema(Relationship):
    src_id: str
    dst_id: str
    rel_kind: str
    since_ts: float | None = None
    until_ts: float | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None

class EntityComponentRef(Relationship):
    component_id: str
    component_type: str | None = None
    label: str | None = None
