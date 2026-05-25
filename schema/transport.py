"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import Communication

### Enums

class Transport_type(IntEnum):
    NETWORK = 0
    CARRIER = auto()
    PROTOCOL = auto()

### Models

class Transport(Communication):
    pass

class RetryProfile(Transport):
    max_attempts: int = 0
    base_delay_ms: int = 0
    backoff_factor: float = 1.0
    jitter_pct: float = 0.0
