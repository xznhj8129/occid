"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class ClassificationLevel(IntEnum):
    UNCLASSIFIED = 0
    CONTROLLED = auto()
    CONFIDENTIAL = auto()
    SECRET = auto()
    TOP_SECRET = auto()

class VideoProtocol(IntEnum):
    RTSP = 0
    RTMP = auto()
    SRT = auto()
    HLS = auto()
    UDP = auto()
    TCP = auto()

class MediaType(IntEnum):
    IMAGE = 0
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    BINARY = auto()

### Models

class ClassificationSchema(OCCIDModel):
    level: ClassificationLevel
    codewords: list[str]
    release_to: list[str]

class VideoConfigSchema(OCCIDModel):
    protocol: VideoProtocol | None = None
    port: int | None = None
    stream_url: str | None = None
    overlay_url: str | None = None
    webrtc_url: str | None = None
    overlay_webrtc_url: str | None = None
    hls_url: str | None = None

class MediaItemSchema(OCCIDModel):
    media_id: str
    media_type: MediaType
    uri: str
    label: str | None = None
    created_ts: float | None = None
    size_bytes: int | None = None
    content_type: str | None = None

class MediaSchema(OCCIDModel):
    items: list[MediaItemSchema]
