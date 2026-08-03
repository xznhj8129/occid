"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Models

class Media(Data):
    'Image, video, audio, document, frame, recording, point cloud, sample block, or binary media reference'
    __occid_model_id__: ClassVar[int] = 74

class MediaItemSchema(Media):
    __occid_model_id__: ClassVar[int] = 75
    record: RecordMeta
    media_id: StringID
    media_type: MediaType
    uri: builtins.str
    label: builtins.str | None = None
    size_bytes: builtins.int | None = None
    content_type: builtins.str | None = None
