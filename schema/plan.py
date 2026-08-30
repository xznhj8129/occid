"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control
from .struct import Struct

### Enums

class PlanApprovalState(IntEnum):
    DRAFT = 0
    PROPOSED = auto()
    APPROVED = auto()
    REJECTED = auto()
    SUPERSEDED = auto()

class PlanStepStatus(IntEnum):
    PENDING = 0
    READY = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    FAILED = auto()
    SKIPPED = auto()

class FlightType(IntEnum):
    SURVEY_POINT = 0
    SURVEY_AREA = auto()
    ONE_WAY = auto()

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

### Models

class Plan(Control):
    'Proposed or approved method for accomplishing one or more tasks using actors, resources, sequencing, routes, constraints, and contingencies'
    __occid_model_id__: ClassVar[int] = 172
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    plan_id: UID
    name: builtins.str | None = None
    objective_ids: list[UID]
    task_ids: list[UID]
    actor_ids: list[UID]
    resource_ids: list[UID]
    assignments: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class PlanStep(Struct):
    'Immutable planned step definition; runtime status belongs to execution state'
    __occid_model_id__: ClassVar[int] = 283
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    step_id: builtins.int
    task_id: UID | None = None
    actor_ids: list[UID]
    depends_on: list[builtins.int]
    sequence: builtins.int

class PlanContingency(Struct):
    __occid_model_id__: ClassVar[int] = 282
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    contingency_id: builtins.int
    condition: SerializeAsAny[Condition | Predicate | BooleanLogic]
    response: builtins.str
    task_ids: list[UID]

class FlightLevelBand(Struct):
    'Embedded flight-level band value used by plans rather than an independently identified control reference'
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    altitude_range_m: NumericRange
    alt_sep_m: builtins.float

class AutopilotMissionWaypoint(Struct):
    'Embedded autopilot waypoint value used by a plan or protocol mapping'
    __occid_model_id__: ClassVar[int] = 118
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    waypoint_index: builtins.int
    action_code: builtins.int | None = None
    position: GlobalPosition
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None

class PlannerMissionPoint(Struct):
    'Embedded planner point value used while constructing a plan'
    __occid_model_id__: ClassVar[int] = 119
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    num: builtins.int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class LoiterOrbit(Struct):
    'Embedded orbit geometry and timing value'
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    orbit_direction: builtins.int
    orbit_radius: builtins.int
    loiter_time: builtins.int

class MissionRouteGeometry(Struct):
    'Embedded route geometry used by a mission plan'
    __occid_model_id__: ClassVar[int] = 121
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class PlannedRoutePoints(Struct):
    'Embedded set of planner points defining mission-plan route segments'
    __occid_model_id__: ClassVar[int] = 122
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint

class AutopilotFlightPlan(Plan):
    __occid_model_id__: ClassVar[int] = 173
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    waypoints: list[AutopilotMissionWaypoint]

class GroupFlightPlan(Plan):
    __occid_model_id__: ClassVar[int] = 174
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    plan_phase: FlightPlanPhase
    flight_level: FlightLevelBand | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: builtins.float | None = None
    delay_s: builtins.float | None = None
    airspeed: builtins.float | None = None
    path_offset: LocalDirection | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class UnitFlightPlan(Plan):
    __occid_model_id__: ClassVar[int] = 175
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    unit_num: builtins.int
    callsign: builtins.str
    fl: builtins.float
    route_in: GeoPath
    target: PlannerMissionPoint
    route_out: GeoPath
    home: GlobalPosition
    land_pos: GlobalPosition
    ip_wait_delay: builtins.float = 0.0
    wp: GeoPath

class MissionPlan(Plan):
    'Saved operator mission plan - the planner inputs, restorable for editing'
    __occid_model_id__: ClassVar[int] = 176
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    flight_type: FlightType = FlightType.SURVEY_POINT
    air_action: AirPlanAction = AirPlanAction.FLY
    manual: builtins.bool = False
    points: PlannedRoutePoints
    config: dict[builtins.str, builtins.float]
    saved_ts: builtins.float | None = None
