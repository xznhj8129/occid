"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Media(OCCIDModel):
    'Image, video, audio, document, frame, recording, point cloud, sample block, or binary media reference'
    __occid_model_id__: ClassVar[int] = 137
    __occid_semantic_role__: ClassVar[str] = 'type'

class MediaItem(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 138
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('MediaItem')]
    media_type: MediaType
    uri: builtins.str
    label: builtins.str | None = None
    size_bytes: builtins.int | None = None
    content_type: builtins.str | None = None
