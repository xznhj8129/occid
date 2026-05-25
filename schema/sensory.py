"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class MediaType(IntEnum):
    IMAGE = 0
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    BINARY = auto()

class SensoryType(IntEnum):
    A_V = 0
    SPATIAL = auto()
    SAMPLES = auto()

### Models

class Sensory(Data):
    pass

class AV(Sensory):
    pass

class Spatial(Sensory):
    pass

class Samples(Sensory):
    pass

class MediaItemSchema(AV):
    media_id: str
    media_type: MediaType
    uri: str
    label: str | None = None
    created_ts: float | None = None
    size_bytes: int | None = None
    content_type: str | None = None

class MediaSchema(AV):
    items: list[MediaItemSchema]
