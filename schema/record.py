"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .struct import Struct

### Models

class RecordMeta(Struct):
    'Persistent-record instance identity, revision, timestamps, origin, classification, and provenance metadata'
    __occid_model_id__: ClassVar[int] = 284
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record_id: UID
    revision: builtins.int = 0
    created_ts: builtins.float
    updated_ts: builtins.float
    origin_system: builtins.str
    classification: builtins.str | None = None
    provenance: list[builtins.str]
