"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ManeuverIntent(IntEnum):
    MOVE = 0
    HOLD = auto()
    FOLLOW = auto()
    TRANSIT = auto()
    POSITION = auto()

class EffectIntent(IntEnum):
    CREATE = 0
    REMOVE = auto()
    MODIFY = auto()
    RESTORE = auto()
    PROTECT = auto()
    DENY = auto()

class InformationIntent(IntEnum):
    SEARCH = 0
    OBSERVE = auto()
    IDENTIFY = auto()
    CLASSIFY = auto()
    MEASURE = auto()
    ASSESS = auto()
    MONITOR = auto()

class TransportIntent(IntEnum):
    CARGO = 0
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

### Models

class Task(OCCIDModel):
    'Directed work that must be accomplished in support of an optional objective'
    __occid_model_id__: ClassVar[int] = 244
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Task')]
    instruction: builtins.str
    target_uids: list[UID]
    location_uids: list[UID]
    objective_uid: UID | None = None
    constraints: list[Constraint]
    preconditions: list[Predicate | BooleanLogic] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    phase: TaskPhase

class TaskManeuver(OCCIDModel):
    'Practical Task schema for desired movement, position, or spatial persistence'
    __occid_model_id__: ClassVar[int] = 248
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Task')]
    instruction: builtins.str
    target_uids: list[UID]
    location_uids: list[UID]
    objective_uid: UID | None = None
    constraints: list[Constraint]
    preconditions: list[Predicate | BooleanLogic] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    phase: TaskPhase
    intent: ManeuverIntent

class TaskEffect(OCCIDModel):
    'Practical Task schema for desired creation, removal, modification, restoration, protection, or denial'
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Task')]
    instruction: builtins.str
    target_uids: list[UID]
    location_uids: list[UID]
    objective_uid: UID | None = None
    constraints: list[Constraint]
    preconditions: list[Predicate | BooleanLogic] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    phase: TaskPhase
    intent: EffectIntent

class TaskInformation(OCCIDModel):
    'Practical Task schema for desired search, observation, identification, classification, measurement, assessment, or monitoring'
    __occid_model_id__: ClassVar[int] = 247
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Task')]
    instruction: builtins.str
    target_uids: list[UID]
    location_uids: list[UID]
    objective_uid: UID | None = None
    constraints: list[Constraint]
    preconditions: list[Predicate | BooleanLogic] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    phase: TaskPhase
    intent: InformationIntent

class TaskTransport(OCCIDModel):
    'Practical Task schema for desired movement of cargo, personnel, supplies, casualties, or recoverable assets'
    __occid_model_id__: ClassVar[int] = 250
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Task')]
    instruction: builtins.str
    target_uids: list[UID]
    location_uids: list[UID]
    objective_uid: UID | None = None
    constraints: list[Constraint]
    preconditions: list[Predicate | BooleanLogic] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    phase: TaskPhase
    intent: TransportIntent
