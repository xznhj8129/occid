"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .directive import Directive

### Enums

class TaskType(IntEnum):
    MANEUVER = 0
    EFFECT = auto()
    INFORMATION = auto()
    TRANSPORT = auto()

class TaskIntent(IntEnum):
    MOVE = 0
    HOLD = auto()
    FOLLOW = auto()
    TRANSIT = auto()
    POSITION = auto()
    CREATE = auto()
    REMOVE = auto()
    MODIFY = auto()
    RESTORE = auto()
    PROTECT = auto()
    DENY = auto()
    SEARCH = auto()
    OBSERVE = auto()
    IDENTIFY = auto()
    CLASSIFY = auto()
    MEASURE = auto()
    ASSESS = auto()
    MONITOR = auto()
    CARGO = auto()
    PERSONNEL = auto()
    SUPPLY = auto()
    EVACUATE = auto()
    RECOVER = auto()

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

### Mappings

VALID_TASK_INTENT_TYPES: dict[TaskIntent, TaskType] = {
    TaskIntent.MOVE: TaskType.MANEUVER,
    TaskIntent.HOLD: TaskType.MANEUVER,
    TaskIntent.FOLLOW: TaskType.MANEUVER,
    TaskIntent.TRANSIT: TaskType.MANEUVER,
    TaskIntent.POSITION: TaskType.MANEUVER,
    TaskIntent.CREATE: TaskType.EFFECT,
    TaskIntent.REMOVE: TaskType.EFFECT,
    TaskIntent.MODIFY: TaskType.EFFECT,
    TaskIntent.RESTORE: TaskType.EFFECT,
    TaskIntent.PROTECT: TaskType.EFFECT,
    TaskIntent.DENY: TaskType.EFFECT,
    TaskIntent.SEARCH: TaskType.INFORMATION,
    TaskIntent.OBSERVE: TaskType.INFORMATION,
    TaskIntent.IDENTIFY: TaskType.INFORMATION,
    TaskIntent.CLASSIFY: TaskType.INFORMATION,
    TaskIntent.MEASURE: TaskType.INFORMATION,
    TaskIntent.ASSESS: TaskType.INFORMATION,
    TaskIntent.MONITOR: TaskType.INFORMATION,
    TaskIntent.CARGO: TaskType.TRANSPORT,
    TaskIntent.PERSONNEL: TaskType.TRANSPORT,
    TaskIntent.SUPPLY: TaskType.TRANSPORT,
    TaskIntent.EVACUATE: TaskType.TRANSPORT,
    TaskIntent.RECOVER: TaskType.TRANSPORT,
}

### Models

class Task(Directive):
    'Generic instruction-bearing work that must be accomplished in support of an optional objective'
    __occid_model_id__: ClassVar[int] = 124
    record: RecordMeta
    task_id: StringID
    instruction: builtins.str
    task_type: TaskType
    task_intent: TaskIntent | None = None
    target_refs: list[StringID]
    location_refs: list[StringID]
    objective_id: StringID | None = None
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | ConstraintCondition | TaskTimeWindow | WeatherLimits]]
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
