"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class Plan(OCCIDModel):
    'Proposed or approved method for accomplishing one or more tasks using actors, resources, sequencing, routes, constraints, and contingencies'
    __occid_model_id__: ClassVar[int] = 183
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class PlanStep(OCCIDModel):
    'Immutable planned step definition; runtime status belongs to execution state'
    __occid_model_id__: ClassVar[int] = 185
    __occid_semantic_role__: ClassVar[str] = 'representation'
    actor_uids: list[UID]
    depends_on: list[builtins.int]
    sequence: builtins.int

class PlanContingency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 184
    __occid_semantic_role__: ClassVar[str] = 'representation'
    condition: Predicate | BooleanLogic
    response: builtins.str
    task_uids: list[UID]

class FlightLevelBand(OCCIDModel):
    'Embedded flight-level band value used by plans rather than an independently identified control reference'
    __occid_model_id__: ClassVar[int] = 77
    __occid_semantic_role__: ClassVar[str] = 'representation'
    altitude_range_m: NumericRange
    alt_sep_m: builtins.float

class AutopilotMissionWaypoint(OCCIDModel):
    'Embedded autopilot waypoint value used by a plan or protocol mapping'
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'representation'
    waypoint_index: builtins.int
    action_code: builtins.int | None = None
    position: GlobalPosition
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None

class PlannerMissionPoint(OCCIDModel):
    'Embedded planner point value used while constructing a plan'
    __occid_model_id__: ClassVar[int] = 187
    __occid_semantic_role__: ClassVar[str] = 'representation'
    num: builtins.int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class LoiterOrbit(OCCIDModel):
    'Embedded orbit geometry and timing value'
    __occid_model_id__: ClassVar[int] = 132
    __occid_semantic_role__: ClassVar[str] = 'representation'
    orbit_direction: builtins.int
    orbit_radius: builtins.int
    loiter_time: builtins.int

class MissionRouteGeometry(OCCIDModel):
    'Embedded route geometry used by a mission plan'
    __occid_model_id__: ClassVar[int] = 157
    __occid_semantic_role__: ClassVar[str] = 'representation'
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class PlannedRoutePoints(OCCIDModel):
    'Embedded set of planner points defining mission-plan route segments'
    __occid_model_id__: ClassVar[int] = 186
    __occid_semantic_role__: ClassVar[str] = 'representation'
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint

class AutopilotFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 16
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    waypoints: list[AutopilotMissionWaypoint]

class GroupFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 98
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    plan_phase: FlightPlanPhase
    flight_level: FlightLevelBand | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: builtins.float | None = None
    delay_s: builtins.float | None = None
    airspeed: builtins.float | None = None
    path_offset: LocalDirection | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class UnitFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 264
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
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

class MissionPlan(OCCIDModel):
    'Saved operator mission plan - the planner inputs, restorable for editing'
    __occid_model_id__: ClassVar[int] = 156
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    flight_type: FlightType = FlightType.SURVEY_POINT
    air_action: AirPlanAction = AirPlanAction.FLY
    manual: builtins.bool = False
    points: PlannedRoutePoints
    config: dict[builtins.str, builtins.float]
    saved_ts: Timestamp | None = None
