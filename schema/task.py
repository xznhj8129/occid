"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control, TaskLevel, TaskPhase, TaskPriority, TaskStatus
from .message import AckMode, ConflictPolicy, DeliveryState, QosTier, RouteMode

### Enums

class TaskISR(IntEnum):
    OBSERVE = 0
    SEARCH = auto()
    FIND = auto()
    SURVEY = auto()
    INVESTIGATE = auto()
    IMPROVE_TRACK = auto()
    IMAGERY = auto()

class Task_type(IntEnum):
    MISSION = 0
    PLAN = auto()
    ISR = auto()
    COMBAT = auto()

### Models

class Task(Control):
    'A directive to accomplish an objective'
    task_id: str
    task_level: TaskLevel
    task_type: TaskType | None = None
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
    status_log: list[TaskStatusEntry]
    qos: QosTier = QosTier.ROUTINE
    ack_mode: AckMode = AckMode.RECEIPT
    route_mode: RouteMode = RouteMode.DIRECT
    conflict_policy: ConflictPolicy = ConflictPolicy.VECTOR_CLOCK
    objective: Objective | None = None

class Mission(Task):
    'Tactical, intent-based task that may contain other tasks'
    task_level: TaskLevel = Field(default=TaskLevel.MISSION, frozen=True)
    tasks: list[SerializeAsAny[Task | Mission | Plan | AutopilotFlightPlan | GroupFlightPlan | UnitFlightPlan | IsrTask]]

class IsrTask(Task):
    isr_task: TaskISR | None = None
    area: GeoArea
    dwell_seconds: float | None = None
    isr_params: IsrParameters | None = None
    isr_result: IsrResult | None = None
