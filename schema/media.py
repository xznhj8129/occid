"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Models

class Media(Data):
    'Image, video, audio, document, frame, recording, point cloud, sample block, or binary media reference'

class MediaItemSchema(Media):
    media_id: str
    media_type: MediaType
    uri: str
    label: str | None = None
    created_ts: float | None = None
    size_bytes: int | None = None
    content_type: str | None = None
