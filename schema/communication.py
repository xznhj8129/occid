"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class SyncState(IntEnum):
    IN_SYNC = 0
    PARTIAL = auto()
    STALE = auto()
    DIVERGED = auto()

class AddressingMode(IntEnum):
    UNICAST = 0
    MULTICAST = auto()
    BROADCAST = auto()

class ExchangePattern(IntEnum):
    PUSH = 0
    REQUEST_RESPONSE = auto()
