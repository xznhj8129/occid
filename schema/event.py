"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class Event(OCCIDModel):
    'A discrete occurrence, planned or unplanned, with subject, source, time, type, and event data'
    __occid_model_id__: ClassVar[int] = 69
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record

class FlightEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 76
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record

class MissionEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 155
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
