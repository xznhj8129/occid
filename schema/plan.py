"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .task import Task, TaskAir, TaskLevel

### Enums

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

### Models

class Plan(Task):
    'Plan-level task with structured execution data and no task subdivision'
    __occid_model_id__: ClassVar[int] = 172
    task_level: TaskLevel = Field(default=TaskLevel.PLAN, frozen=True)

class AutopilotFlightPlan(Plan):
    __occid_model_id__: ClassVar[int] = 173
    waypoints: list[AutopilotMissionWaypoint]

class GroupFlightPlan(Plan):
    __occid_model_id__: ClassVar[int] = 174
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
    name: builtins.str
    flight_type: FlightType = FlightType.SURVEY_POINT
    air_task: TaskAir = TaskAir.FLY
    manual: builtins.bool = False
    points: PlannedRoutePoints
    config: dict[builtins.str, builtins.float]
    saved_ts: builtins.float | None = None
