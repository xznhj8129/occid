"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import AckMode, ConflictPolicy, DeliveryState, QosTier, RouteMode

### Enums

class Capability(IntEnum):
    NONE = 0
    DIRECT_FIRES = auto()
    INDIRECT_FIRES = auto()
    LOGISTICS_SUPPLY = auto()
    COMMUNICATIONS = auto()
    FUEL = auto()
    RESCUE = auto()
    SURVEILLANCE = auto()

class TaskType(IntEnum):
    POSITIONING = 0
    COMBAT = auto()
    ISR = auto()
    CARGO = auto()
    HOLD = auto()
    SUPPORT = auto()
    MOVE = auto()
    RESUPPLY = auto()

class TaskCombat(IntEnum):
    DEFEND = 0
    ATTACK = auto()
    PROTECT = auto()
    COMBAT_SUPPORT = auto()
    COMBAT_RESERVE = auto()

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

### Models

class MunitionAllocation(OCCIDModel):
    munition_type: str
    qty: int = '0'

class TaskTimeWindow(OCCIDModel):
    earliest_start: float | None = None
    latest_finish: float | None = None

class ObjectiveSchema(OCCIDModel):
    objective_id: str
    intent: str
    success_rule: str | None = None
    priority: TaskPriority | None = None
    target_ref: str | None = None
    geo_goal: GlobalPosition | None = None
    end_condition: str | None = None
    deadline_ts: float | None = None

class ObjectiveBinding(OCCIDModel):
    objective_id: str
    task_ids: list[str] = Field(default_factory=list)
    priority: TaskPriority | None = None
    deadline_ts: float | None = None
    success_rule: str | None = None

class TaskDelta(OCCIDModel):
    task_id: str
    task_rev: int = '0'
    phase: TaskPhase
    progress: float | None = None
    owner: str | None = None
    updated_ts: float

class TaskStatusEntry(OCCIDModel):
    ts: float
    status: TaskStatus
    command_result: CommandResult | None = None
    reply_ack: ReplyAck | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase | None = None
    detail: str | None = None
    source: str | None = None

class BaseTask(OCCIDModel):
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
    assigned_assets: list[str] = Field(default_factory=list)
    attempt_idx: int = '0'
    dispatch_state: DeliveryState = DeliveryState.QUEUED
    dispatch_error: str | None = None
    time_window: TaskTimeWindow | None = None
    retry_profile: RetryProfile | None = None
    status_log: list[TaskStatusEntry] = Field(default_factory=list)
    qos: QosTier = QosTier.ROUTINE
    ack_mode: AckMode = AckMode.RECEIPT
    route_mode: RouteMode = RouteMode.DIRECT
    conflict_policy: ConflictPolicy = ConflictPolicy.VECTOR_CLOCK
    objective: ObjectiveSchema | None = None

class VehicleCommand(OCCIDModel):
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

class MoveTask(BaseTask):
    task_type: TaskType = Field(default=TaskType.MOVE, frozen=True)
    movement_domain: OperationalDomain
    destination: GlobalPosition
    route: GeoPath | None = None
    speed_ms: float | None = None

class CombatTask(BaseTask):
    task_type: TaskType = Field(default=TaskType.COMBAT, frozen=True)
    strike_task: TaskCombat | None = None
    target_category: TargetCategory | None = None
    target_point: GlobalPosition | None = None
    munitions: list[MunitionAllocation] = Field(default_factory=list)
    effect: str | None = None
    desired_bda: bool = 'false'

class ResupplyTask(BaseTask):
    task_type: TaskType = Field(default=TaskType.RESUPPLY, frozen=True)
    destination: GlobalPosition
    payload: list[PayloadAllocation] = Field(default_factory=list)
    payload_plan: PayloadPlanSchema | None = None
