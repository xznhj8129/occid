"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Record(OCCIDModel):
    'Persistent Record UID, class-local Record ID, revision, timestamps, origin, classification, and provenance metadata'
    __occid_model_id__: ClassVar[int] = 218
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Record')]
    revision: builtins.int = 0
    created_ts: Semantic[Timestamp]
    updated_ts: Semantic[Timestamp]
    origin_system: builtins.str
    provenance: list[builtins.str]
