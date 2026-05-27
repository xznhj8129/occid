"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control, TaskPhase, TaskPriority, TaskStatus, TaskType
from .message import AckMode, ConflictPolicy, DeliveryState, QosTier, RouteMode

### Enums

class Directive_type(IntEnum):
    MISSION = 0
    TASK = auto()
    COMMAND = auto()

class Task_type(IntEnum):
    MOVE = 0
    RESUPPLY = auto()
    ISR = auto()
    COMBAT = auto()

### Models

class Directive(Control):
    'Ordered or requested work, including missions, tasks, and immediate commands'

class Mission(Directive):
    pass

class Command(Directive):
    pass

class MissionProgress(Mission):
    waypoint_count: int | None = None
    current_waypoint_index: int | None = None
    mission_valid: bool | None = None

class Task(Directive):
    'A directive to carry out part of a mission'
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
