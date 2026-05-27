"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class SyncState(IntEnum):
    IN_SYNC = 0
    PARTIAL = auto()
    STALE = auto()
    DIVERGED = auto()

class Communication_type(IntEnum):
    NODE = 0
    TRANSPORT = auto()
    FEED = auto()
    MESSAGE = auto()

### Models

class Communication(Root):
    'Movement of information between endpoints'
