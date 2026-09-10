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

class NATOAlphabet(IntEnum):
    ALPHA = 0
    BRAVO = auto()
    CHARLIE = auto()
    DELTA = auto()
    ECHO = auto()
    FOXTROT = auto()
    GOLF = auto()
    HOTEL = auto()
    INDIA = auto()
    JULIETT = auto()
    KILO = auto()
    LIMA = auto()
    MIKE = auto()
    NOVEMBER = auto()
    OSCAR = auto()
    PAPA = auto()
    QUEBEC = auto()
    ROMEO = auto()
    SIERRA = auto()
    TANGO = auto()
    UNIFORM = auto()
    VICTOR = auto()
    WHISKEY = auto()
    XRAY = auto()
    YANKEE = auto()
    ZULU = auto()

### Models

class Communication(OCCIDModel):
    'Movement of information between endpoints'
    __occid_model_id__: ClassVar[int] = 60
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Interface', 'Link', 'DataRateSpec', 'LinkCapacity', 'Message', 'Network', 'Node', 'Protocol')
