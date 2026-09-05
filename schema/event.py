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
    __occid_model_id__: ClassVar[int] = 78
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightEvent', 'MissionEvent')
    record: Semantic[Record]

class FlightEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 85
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]

class MissionEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 167
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
