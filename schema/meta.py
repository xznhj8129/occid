"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Models

class DisplayMeta(OCCIDModel):
    icon_code: str | None = None
    tint: str | None = None
    short_label: str | None = None

class RelationSchema(OCCIDModel):
    src_id: str
    dst_id: str
    rel_kind: str
    since_ts: float | None = None
    until_ts: float | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None
