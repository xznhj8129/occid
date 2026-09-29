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
    'A discrete occurrence; concrete event representations define the subject, time, vocabulary, and event-specific data appropriate to that semantic branch'
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SubjectEvent', 'TimelineEvent')

class SubjectEvent(OCCIDModel):
    'Event concerning one identified operational subject at one semantic timestamp'
    __occid_model_id__: ClassVar[int] = 312
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightEvent', 'MissionEvent')
    subject_uid: Semantic[ID]
    timestamp: Semantic[Timestamp]

class FlightEvent(OCCIDModel):
    'Flight or air-mission lifecycle occurrence for an identified subject'
    __occid_model_id__: ClassVar[int] = 110
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectEvent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[ID]
    timestamp: Semantic[Timestamp]
    event: AirMissionEvent

class MissionEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 210
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectEvent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[ID]
    timestamp: Semantic[Timestamp]

class TimelineEvent(OCCIDModel):
    'Human-authored or imported operational timeline occurrence used for scenario, rehearsal, planning, and historical presentation'
    __occid_model_id__: ClassVar[int] = 338
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    description: Semantic[Text] | None = None
    temporal_extent: Semantic[TimeRange]
    context_uid: Semantic[ID] | None = None
    subject_uids: list[Semantic[ID]]
    location_uids: list[Semantic[ID]]
    media_uids: list[Semantic[ID]]
