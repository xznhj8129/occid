"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Enums

class AirMissionEvent(IntEnum):
    ONLINE = 0
    PREPARED = auto()
    LOADED = auto()
    READY_TAKEOFF = auto()
    TAKEOFF_COMPLETE = auto()
    ASSEMBLY = auto()
    ENROUTE = auto()
    HOLDING = auto()
    ACTING = auto()
    PROCEEDING = auto()
    RESUMING = auto()
    BINGO = auto()
    RTB = auto()
    LANDING = auto()
    LANDED = auto()
    SHUTDOWN = auto()
    ABORTING = auto()
    FAILING = auto()

### Models

class Event(Data):
    'A discrete occurrence, planned or unplanned, with subject, source, time, type, and event data'
    __occid_model_id__: ClassVar[int] = 66
    record: RecordMeta

class FlightEvent(Event):
    __occid_model_id__: ClassVar[int] = 67

class MissionEvent(Event):
    __occid_model_id__: ClassVar[int] = 68
