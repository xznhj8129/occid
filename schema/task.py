"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Enums

class TaskISR(IntEnum):
    OBSERVE = 0
    SEARCH = auto()
    FIND = auto()
    SURVEY = auto()
    INVESTIGATE = auto()
    IMPROVE_TRACK = auto()
    IMAGERY = auto()

class TaskType(IntEnum):
    POSITIONING = 0
    CARGO = auto()
    HOLD = auto()
    SUPPORT = auto()
    MOVE = auto()
    RESUPPLY = auto()

class TaskLevel(IntEnum):
    MISSION = 0
    PLAN = auto()

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

class TaskAir(IntEnum):
    FLY = 0
    AIR_DROP = auto()
    RECOVERY = auto()

class AirMoveTask(IntEnum):
    FLY = 0
    RELOCATION = auto()

### Models

class Task(Control):
    'A directive to accomplish an objective'
    __occid_model_id__: ClassVar[int] = 124
    task_id: StringID
    task_level: TaskLevel
    task_type: TaskType | None = None
    status: TaskStatus = TaskStatus.NEW
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE

class Mission(Task):
    'Tactical, intent-based task that may contain other tasks'
    __occid_model_id__: ClassVar[int] = 125
    task_level: TaskLevel = Field(default=TaskLevel.MISSION, frozen=True)
    tasks: list[SerializeAsAny[Task | Mission | Plan | AutopilotFlightPlan | GroupFlightPlan | UnitFlightPlan | MissionPlan | IsrTask | MoveTask | HoldTask | ResupplyTask]]

class IsrTask(Task):
    __occid_model_id__: ClassVar[int] = 126
    isr_task: TaskISR | None = None
    area: GeoArea
    dwell_seconds: builtins.float | None = None
    isr_params: IsrParameters | None = None
    isr_result: IsrResult | None = None

class MoveTask(Task):
    'Reposition to a destination; the entity resolves how'
    __occid_model_id__: ClassVar[int] = 127
    task_type: TaskType = Field(default=TaskType.MOVE, frozen=True)
    destination: GlobalPosition
    route: GeoPath | None = None
    speed_ms: builtins.float | None = None
    altitude_m: builtins.float | None = None
    hold_seconds: builtins.float | None = None

class HoldTask(Task):
    'Hold position within a radius of a location'
    __occid_model_id__: ClassVar[int] = 128
    task_type: TaskType = Field(default=TaskType.HOLD, frozen=True)
    location: GlobalPosition
    radius_m: builtins.float

class ResupplyTask(Task):
    'Deliver a payload to a destination'
    __occid_model_id__: ClassVar[int] = 129
    task_type: TaskType = Field(default=TaskType.RESUPPLY, frozen=True)
    destination: GlobalPosition
    payload: dict[builtins.str, builtins.int]
