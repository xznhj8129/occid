"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Media(OCCIDModel):
    'Image, video, audio, document, frame, recording, point cloud, sample block, or binary media reference'
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MediaItem',)

class MediaItem(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 149
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Media'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    media_type: MediaType
    uri: builtins.str
    label: builtins.str | None = None
    size_bytes: builtins.int | None = None
    content_type: builtins.str | None = None
