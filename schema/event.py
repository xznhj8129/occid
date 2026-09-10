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
    __occid_model_id__: ClassVar[int] = 113
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SubjectEvent', 'TimelineEvent')
    record: Semantic[Record]

class SubjectEvent(OCCIDModel):
    'Event concerning one identified operational subject at one semantic timestamp'
    __occid_model_id__: ClassVar[int] = 359
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightEvent', 'MissionEvent')
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]

class FlightEvent(OCCIDModel):
    'Flight or air-mission lifecycle occurrence for an identified subject'
    __occid_model_id__: ClassVar[int] = 122
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectEvent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    event: AirMissionEvent

class MissionEvent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 242
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectEvent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]

class TimelineEvent(OCCIDModel):
    'Human-authored or imported operational timeline occurrence used for scenario, rehearsal, planning, and historical presentation'
    __occid_model_id__: ClassVar[int] = 388
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Event'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Event')]
    name: builtins.str | None = None
    description: Semantic[Text] | None = None
    temporal_extent: Semantic[TimeRange]
    context_uid: Semantic[UID] | None = None
    subject_uids: list[Semantic[UID]]
    location_uids: list[Semantic[UID]]
    media_uids: list[Semantic[UID]]
