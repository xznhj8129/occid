"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .plan import PlanApprovalState

### Enums

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

class FlightType(IntEnum):
    SURVEY_POINT = 0
    SURVEY_AREA = auto()
    ONE_WAY = auto()

class OrbitPattern(IntEnum):
    CIRCLE = 0
    RACETRACK = auto()
    FIGURE_EIGHT = auto()

class FlightPlanPointType(IntEnum):
    HOME = 0
    TAKEOFF = auto()
    LANDING = auto()
    HOLD = auto()
    WAYPOINT = auto()
    ASSEMBLY = auto()
    POI = auto()
    ROI = auto()
    SURVEY = auto()

class PlannerPointCategory(IntEnum):
    ROUTE_IN = 0
    SURVEY = auto()
    SURVEY_AREA = auto()
    ROUTE_OUT = auto()

class AirGroupFormation3DType(IntEnum):
    NONE = 0
    BOX = auto()
    SEP_2D_PER_FL = auto()
    SEP_2D_SPACED = auto()

class AirGroupFormation2DType(IntEnum):
    NONE = 0
    LINE = auto()
    ECHELON = auto()
    TRAIL = auto()
    SQUARE = auto()
    DIAMOND = auto()
    VEE = auto()
    HEAVY_LEFT = auto()
    HEAVY_RIGHT = auto()
    ECHELON_LEFT = auto()
    ECHELON_RIGHT = auto()
    STAGG_TRAIL_LEFT = auto()
    STAGG_TRAIL_RIGHT = auto()

### Models

class AirPlan(OCCIDModel):
    'Plan applicable to aerial operations and flight'
    __occid_model_id__: ClassVar[int] = 7
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GroupFlightPlan', 'UnitFlightPlan', 'PlannedAirMission')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class GroupFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AirPlan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    plan_phase: FlightPlanPhase
    flight_level: Semantic[FlightLevelBand] | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: builtins.float | None = None
    delay_s: builtins.float | None = None
    airspeed: builtins.float | None = None
    path_offset: Semantic[LocalDirection] | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class UnitFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 284
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AirPlan'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryUnitFlightPlan',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    unit_num: builtins.int
    callsign: builtins.str
    fl: builtins.float
    route_in: Semantic[GeoPath]
    target: Semantic[FlightMissionPoint]
    route_out: Semantic[GeoPath]
    home: Semantic[GlobalPosition]
    land_pos: Semantic[GlobalPosition]
    ip_wait_delay: builtins.float = 0.0
    wp: Semantic[GeoPath]

class PlannedAirMission(OCCIDModel):
    'Saved operator mission plan - the planner inputs, restorable for editing'
    __occid_model_id__: ClassVar[int] = 201
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AirPlan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    flight_type: FlightType = FlightType.SURVEY_POINT
    air_action: AirPlanAction = AirPlanAction.FLY
    manual: builtins.bool = False
    points: Semantic[PlannedRoutePoints]
    config: dict[builtins.str, builtins.float]
    saved_ts: Semantic[Timestamp] | None = None

class FlightLevelBand(OCCIDModel):
    'Embedded flight-level band value used by plans rather than an independently identified control reference'
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    altitude_range_m: Semantic[NumericRange]
    alt_sep_m: builtins.float

class LoiterOrbit(OCCIDModel):
    'Embedded orbit geometry and timing value'
    __occid_model_id__: ClassVar[int] = 144
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    orbit_direction_ccw: builtins.bool
    orbit_radius_m: builtins.int
    loiter_time_s: builtins.int
    pattern: OrbitPattern

class MissionRouteGeometry(OCCIDModel):
    'Embedded route geometry used by a mission plan'
    __occid_model_id__: ClassVar[int] = 170
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    route_in: Semantic[GeoPath]
    survey: Semantic[GeoPath]
    survey_area: Semantic[GeoArea]
    route_out: Semantic[GeoPath]

class FlightMissionPoint(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 88
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AutopilotMissionWaypoint'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    waypoint_index: builtins.int
    position: Semantic[GlobalPosition]
    action_code: builtins.int | None = None
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None
    point_type: FlightPlanPointType
    category: PlannerPointCategory

class PlannedRoutePoints(OCCIDModel):
    'Embedded set of planner points defining mission-plan route segments'
    __occid_model_id__: ClassVar[int] = 202
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    start: Semantic[FlightMissionPoint]
    route_in: list[Semantic[FlightMissionPoint]]
    route_out: list[Semantic[FlightMissionPoint]]
    end: Semantic[FlightMissionPoint]
