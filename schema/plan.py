"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .task import Task, TaskLevel

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

class Plan_type(IntEnum):
    AUTOPILOT_FLIGHT = 0
    GROUP_FLIGHT = auto()
    UNIT_FLIGHT = auto()

class UnitFlightPlan_type(IntEnum):
    MILITARY = 0

### Models

class Plan(Task):
    'Plan-level task with structured execution data and no task subdivision'
    task_level: TaskLevel = Field(default=TaskLevel.PLAN, frozen=True)

class AutopilotFlightPlan(Plan):
    waypoints: list[AutopilotMissionWaypoint]

class GroupFlightPlan(Plan):
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
