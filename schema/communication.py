"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Enums

class SyncState(IntEnum):
    IN_SYNC = 0
    PARTIAL = auto()
    STALE = auto()
    DIVERGED = auto()

### Models

class Communication(Root):
    'Movement of information between endpoints'
    __occid_model_id__: ClassVar[int] = 1
