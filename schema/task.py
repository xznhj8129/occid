"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import AckMode, ConflictPolicy, DeliveryState, QosTier, RouteMode
from .directive import Command, Directive, Mission

### Enums

class Capability(IntEnum):
    NONE = 0
    LOGISTICS_SUPPLY = auto()
    COMMUNICATIONS = auto()
    FUEL = auto()
    RESCUE = auto()

class TaskType(IntEnum):
    POSITIONING = 0
    CARGO = auto()
    HOLD = auto()
    SUPPORT = auto()
    MOVE = auto()
    RESUPPLY = auto()

class TaskPhase(IntEnum):
    CREATED = 0
    DISPATCHED = auto()
    ASSIGNED = auto()
    RUNNING = auto()
    DONE_OK = auto()
    DONE_FAIL = auto()
    CANCELLED = auto()

class TaskPriority(IntEnum):
    ROUTINE = 0
    HIGH = auto()
    IMMEDIATE = auto()

class TaskStatus(IntEnum):
    NEW = 0
    ACCEPTED = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    FAILED = auto()
    CANCELLED = auto()

class TaskAssignFail(IntEnum):
    FAIL = 0
    FAIL_NO_ASSETS = auto()
    FAIL_BAD_REQUEST_CANTPRO = auto()
    FAIL_DENIED = auto()
    FAIL_INSUFFICIENT_INFO = auto()
    FAIL_REJECTED = auto()
    FAIL_C2_ELEMENT = auto()
    FAIL_PLATFORM_CANTCO = auto()
    FAIL_STALE = auto()
    FAIL_CANCELLED = auto()

class CommandResult(IntEnum):
    ACCEPTED = 0
    TEMPORARILY_REJECTED = auto()
    DENIED = auto()
    UNSUPPORTED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()
    CANCELLED = auto()

class FlightCommandType(IntEnum):
    ARM = 0
    DISARM = auto()
    TAKEOFF = auto()
    LAND = auto()
    RETURN_TO_LAUNCH = auto()
    SET_MODE = auto()
    GOTO = auto()
    SET_TAKEOFF_ALTITUDE = auto()
    SELECT_MISSION = auto()
    START_OFFBOARD = auto()
    STOP_OFFBOARD = auto()

class TaskAir(IntEnum):
    FLY = 0
    AIR_DROP = auto()
    RECOVERY = auto()

class AirMissionType(IntEnum):
    SURVEY = 0
    SEARCH = auto()
    DELIVERY = auto()

class AirMoveTask(IntEnum):
    FLY = 0
    RELOCATION = auto()

class Task_type(IntEnum):
    MOVE = 0
    RESUPPLY = auto()
    ISR = auto()
    COMBAT = auto()

### Models

class Task(Directive):
    task_id: str
    task_type: TaskType
    unit_code: str
    capability: Capability | None = None
    status: TaskStatus = TaskStatus.NEW
    command_result: CommandResult | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase = TaskPhase.CREATED
    geometry_id: str | None = None
    start_time: float | None = None
    deadline: float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    remarks: str | None = None
    last_update: float | None = None
    issued_by: str | None = None
    accepted_by: str | None = None
    assigned_assets: list[str]
    attempt_idx: int = 0
    dispatch_state: DeliveryState = DeliveryState.QUEUED
    dispatch_error: str | None = None
    time_window: TaskTimeWindow | None = None
    retry_profile: RetryProfile | None = None
    status_log: list[TaskStatusEntry]
    qos: QosTier = QosTier.ROUTINE
    ack_mode: AckMode = AckMode.RECEIPT
    route_mode: RouteMode = RouteMode.DIRECT
    conflict_policy: ConflictPolicy = ConflictPolicy.VECTOR_CLOCK
    objective: ObjectiveSchema | None = None

class VehicleCommand(Command):
    command_id: str
    command_type: FlightCommandType
    asset_id: str
    mode: str | None = None
    enabled: bool | None = None
    altitude_m: float | None = None
    yaw_deg: float | None = None
    destination: GlobalPosition | None = None
    waypoint: AutopilotMissionWaypoint | None = None
    sequence: int | None = None
    control_override: ControlOverride | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None

class TrackerCommand(Command):
    lock: bool | None = None
    reset: bool | None = None
    slew: LocalDirection | None = None
    search_box_size: int | None = None
    shutdown: bool | None = None

class MoveTask(Task):
    task_type: TaskType = Field(default=TaskType.MOVE, frozen=True)
    movement_domain: OperationalDomain
    destination: GlobalPosition
    route: GeoPath | None = None
    speed_ms: float | None = None

class ResupplyTask(Task):
    task_type: TaskType = Field(default=TaskType.RESUPPLY, frozen=True)
    destination: GlobalPosition
    supplies: list[ItemCount]

class AirMissionSchema(Mission):
    mission_name: str
    mission_uid: str
    mission_time: float
    mission_type: TaskType
    takeoff: FlightPhasePlan
    assembly_point: FlightPhasePlan
    route: FlightPhasePlan
    ingress: FlightPhasePlan
    survey_area: FlightPhasePlan
    egress: FlightPhasePlan
    landing: FlightPhasePlan
    pois: list[MissionPoi]
    assignments: dict[str, FlightAssignment]
    unit_plans: dict[str, PlannedUnitMission]
    routes: MissionRouteGeometry
    route_points: PlannedRoutePoints
