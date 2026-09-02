"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Record(OCCIDModel):
    'Persistent Record UID, class-local Record ID, revision, timestamps, origin, classification, and provenance metadata'
    __occid_model_id__: ClassVar[int] = 202
    __occid_semantic_role__: ClassVar[str] = 'representation'
    uid: UID
    id: Annotated[IntID, IDNamespace('Record')]
    revision: builtins.int = 0
    created_ts: builtins.float
    updated_ts: builtins.float
    origin_system: builtins.str
    classification: builtins.str | None = None
    provenance: list[builtins.str]
