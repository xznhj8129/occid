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
    __occid_model_id__: ClassVar[int] = 197
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AutopilotFlightPlan', 'GroupFlightPlan', 'UnitFlightPlan', 'MissionPlan')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[Semantic[UID]]
    task_uids: list[Semantic[UID]]
    actor_uids: list[Semantic[UID]]
    resource_uids: list[Semantic[UID]]
    assignment_uids: list[Semantic[UID]]
    steps: list[Semantic[PlanStep]]
    routes: list[Semantic[GeoPath]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class PlanStep(OCCIDModel):
    'Immutable planned step definition; runtime status belongs to execution state'
    __occid_model_id__: ClassVar[int] = 199
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    actor_uids: list[Semantic[UID]]
    depends_on: list[builtins.int]
    sequence: builtins.int

class PlanContingency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 198
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition]
    response: builtins.str
    task_uids: list[Semantic[UID]]

class FlightLevelBand(OCCIDModel):
    'Embedded flight-level band value used by plans rather than an independently identified control reference'
    __occid_model_id__: ClassVar[int] = 86
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    altitude_range_m: Semantic[NumericRange]
    alt_sep_m: builtins.float

class AutopilotMissionWaypoint(OCCIDModel):
    'Embedded autopilot waypoint value used by a plan or protocol mapping'
    __occid_model_id__: ClassVar[int] = 19
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    waypoint_index: builtins.int
    action_code: builtins.int | None = None
    position: Semantic[GlobalPosition]
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None

class PlannerMissionPoint(OCCIDModel):
    'Embedded planner point value used while constructing a plan'
    __occid_model_id__: ClassVar[int] = 201
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    num: builtins.int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: Semantic[GlobalPosition]

class LoiterOrbit(OCCIDModel):
    'Embedded orbit geometry and timing value'
    __occid_model_id__: ClassVar[int] = 142
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    orbit_direction: builtins.int
    orbit_radius: builtins.int
    loiter_time: builtins.int

class MissionRouteGeometry(OCCIDModel):
    'Embedded route geometry used by a mission plan'
    __occid_model_id__: ClassVar[int] = 169
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    route_in: Semantic[GeoPath]
    survey: Semantic[GeoPath]
    survey_area: Semantic[GeoArea]
    route_out: Semantic[GeoPath]

class PlannedRoutePoints(OCCIDModel):
    'Embedded set of planner points defining mission-plan route segments'
    __occid_model_id__: ClassVar[int] = 200
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    start: Semantic[PlannerMissionPoint]
    route_in: list[Semantic[PlannerMissionPoint]]
    survey: list[Semantic[PlannerMissionPoint]]
    survey_area: list[Semantic[PlannerMissionPoint]]
    route_out: list[Semantic[PlannerMissionPoint]]
    end: Semantic[PlannerMissionPoint]

class AutopilotFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 17
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[Semantic[UID]]
    task_uids: list[Semantic[UID]]
    actor_uids: list[Semantic[UID]]
    resource_uids: list[Semantic[UID]]
    assignment_uids: list[Semantic[UID]]
    steps: list[Semantic[PlanStep]]
    routes: list[Semantic[GeoPath]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    waypoints: list[Semantic[AutopilotMissionWaypoint]]

class GroupFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 107
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[Semantic[UID]]
    task_uids: list[Semantic[UID]]
    actor_uids: list[Semantic[UID]]
    resource_uids: list[Semantic[UID]]
    assignment_uids: list[Semantic[UID]]
    steps: list[Semantic[PlanStep]]
    routes: list[Semantic[GeoPath]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]
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
    __occid_model_id__: ClassVar[int] = 282
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryUnitFlightPlan',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[Semantic[UID]]
    task_uids: list[Semantic[UID]]
    actor_uids: list[Semantic[UID]]
    resource_uids: list[Semantic[UID]]
    assignment_uids: list[Semantic[UID]]
    steps: list[Semantic[PlanStep]]
    routes: list[Semantic[GeoPath]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    unit_num: builtins.int
    callsign: builtins.str
    fl: builtins.float
    route_in: Semantic[GeoPath]
    target: Semantic[PlannerMissionPoint]
    route_out: Semantic[GeoPath]
    home: Semantic[GlobalPosition]
    land_pos: Semantic[GlobalPosition]
    ip_wait_delay: builtins.float = 0.0
    wp: Semantic[GeoPath]

class MissionPlan(OCCIDModel):
    'Saved operator mission plan - the planner inputs, restorable for editing'
    __occid_model_id__: ClassVar[int] = 168
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[Semantic[UID]]
    task_uids: list[Semantic[UID]]
    actor_uids: list[Semantic[UID]]
    resource_uids: list[Semantic[UID]]
    assignment_uids: list[Semantic[UID]]
    steps: list[Semantic[PlanStep]]
    routes: list[Semantic[GeoPath]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    flight_type: FlightType = FlightType.SURVEY_POINT
    air_action: AirPlanAction = AirPlanAction.FLY
    manual: builtins.bool = False
    points: Semantic[PlannedRoutePoints]
    config: dict[builtins.str, builtins.float]
    saved_ts: Semantic[Timestamp] | None = None
