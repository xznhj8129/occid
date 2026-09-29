"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .plan import PlanApprovalState

### Enums

class AirRole(IntEnum):
    GROUND = 0
    AIR_DEFENSE = auto()
    FIGHTER = auto()
    GROUND_ATTACK = auto()
    ISR = auto()
    MINE = auto()
    CARGO = auto()

class FormationPattern(IntEnum):
    LINE = 0
    ECHELON = auto()
    TRAIL = auto()
    SQUARE = auto()
    DIAMOND = auto()
    VEE = auto()
    MISSING_MAN = auto()
    HEAVY_LEFT = auto()
    HEAVY_RIGHT = auto()
    ECHELON_LEFT = auto()
    ECHELON_RIGHT = auto()
    STAGGERED_TRAIL_LEFT = auto()
    STAGGERED_TRAIL_RIGHT = auto()

class FormationRole(IntEnum):
    LEAD = 0
    FOLLOWER = auto()

class FormationJoinState(IntEnum):
    UNKNOWN = 0
    JOINING = auto()
    JOINED = auto()
    LEAVING = auto()
    ABSENT = auto()

class FlightPlanPhase(IntEnum):
    ONLINE = 0
    PREPARING = auto()
    TAKEOFF = auto()
    ASSEMBLY = auto()
    HOLDING = auto()
    ENROUTE = auto()
    INITIAL = auto()
    OBJECTIVE = auto()
    EGRESS = auto()
    RETURN = auto()
    APPROACH = auto()
    LANDING = auto()
    SHUTDOWN = auto()

class AirPlanAction(IntEnum):
    FLY = 0
    AIR_DROP = auto()
    RECOVERY = auto()

class MilitaryAirTask(IntEnum):
    ISR = 0
    CLOSE_AIR_SUPPORT = auto()
    ELECTRONIC_WARFARE = auto()
    STRIKE = auto()
    SEAD = auto()

class AirISRType(IntEnum):
    OVERFLY = 0
    FLYBY = auto()
    ORBIT = auto()

### Models

class FormationStation(OCCIDModel):
    "One element's station, role, and timing within a formation"
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    element_uid: Semantic[ID]
    role: FormationRole
    station_index: builtins.int | None = None
    lateral_offset: Semantic[DistanceMeters] | None = None
    vertical_offset: Semantic[DistanceMeters] | None = None
    longitudinal_offset: Semantic[DistanceMeters] | None = None
    altitude_offset: Semantic[DistanceMeters] | None = None
    delay: Semantic[Duration] | None = None

class Formation(OCCIDModel):
    'Formation definition for a group, including member stations and stream timing'
    __occid_model_id__: ClassVar[int] = 114
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    pattern: FormationPattern
    lateral_separation: Semantic[DistanceMeters]
    vertical_separation: Semantic[DistanceMeters] | None = None
    altitude_offset: Semantic[DistanceMeters] | None = None
    altitude_datum: AltitudeDatum | None = None
    element_interval: Semantic[Duration] | None = None
    stations: list[Semantic[FormationStation]]

class GroupFlightPlan(OCCIDModel):
    'Flight plan for a group flying a route in formation'
    __occid_model_id__: ClassVar[int] = 142
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RoutePlan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    waypoints: list[Semantic[Waypoint]]
    action: AirPlanAction = AirPlanAction.FLY
    home: Semantic[GlobalPosition] | None = None
    flight_level: Semantic[NumericRange] | None = None
    cruise_airspeed: Semantic[Airspeed] | None = None
    formation: Semantic[Formation] | None = None

class FormationElementState(OCCIDModel):
    "One element's observed position, deviation, and join state within a formation"
    __occid_model_id__: ClassVar[int] = 115
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    element_uid: Semantic[ID]
    join_state: FormationJoinState
    position: Semantic[GlobalPosition] | None = None
    lateral_offset: Semantic[DistanceMeters] | None = None
    vertical_offset: Semantic[DistanceMeters] | None = None
    longitudinal_offset: Semantic[DistanceMeters] | None = None

class FormationState(OCCIDModel):
    'Time-indexed formation condition for one plan, one entry per element'
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[ID]
    timestamp: Semantic[Timestamp]
    elements: list[Semantic[FormationElementState]]

class FlightState(OCCIDModel):
    'Time-indexed flight phase and active waypoint for one plan'
    __occid_model_id__: ClassVar[int] = 112
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[ID]
    timestamp: Semantic[Timestamp]
    phase: FlightPlanPhase
    active_waypoint_index: builtins.int | None = None
