"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .directive import Directive

### Enums

class ManeuverIntent(str, Enum):
    __occid_semantic_role__ = 'vocabulary'
    MOVE = 'MOVE'
    HOLD = 'HOLD'
    FOLLOW = 'FOLLOW'
    TRANSIT = 'TRANSIT'
    POSITION = 'POSITION'

class EffectIntent(str, Enum):
    __occid_semantic_role__ = 'vocabulary'
    CREATE = 'CREATE'
    REMOVE = 'REMOVE'
    MODIFY = 'MODIFY'
    RESTORE = 'RESTORE'
    PROTECT = 'PROTECT'
    DENY = 'DENY'

class InformationIntent(str, Enum):
    __occid_semantic_role__ = 'vocabulary'
    SEARCH = 'SEARCH'
    OBSERVE = 'OBSERVE'
    IDENTIFY = 'IDENTIFY'
    CLASSIFY = 'CLASSIFY'
    MEASURE = 'MEASURE'
    ASSESS = 'ASSESS'
    MONITOR = 'MONITOR'

class TransportIntent(str, Enum):
    __occid_semantic_role__ = 'vocabulary'
    CARGO = 'CARGO'
    PERSONNEL = 'PERSONNEL'
    SUPPLY = 'SUPPLY'
    EVACUATE = 'EVACUATE'
    RECOVER = 'RECOVER'

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

class Task(Directive):
    'Directed work that must be accomplished in support of an optional objective'
    __occid_model_id__: ClassVar[int] = 124
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    task_id: StringID
    instruction: builtins.str
    target_refs: list[StringID]
    location_refs: list[StringID]
    objective_id: StringID | None = None
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    preconditions: list[SerializeAsAny[Condition | Predicate | Conjunction | Disjunction | Negation]] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

class TaskManeuver(Task):
    'Practical Task schema for desired movement, position, or spatial persistence'
    __occid_model_id__: ClassVar[int] = 310
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    intent: ManeuverIntent

class TaskEffect(Task):
    'Practical Task schema for desired creation, removal, modification, restoration, protection, or denial'
    __occid_model_id__: ClassVar[int] = 311
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    intent: EffectIntent

class TaskInformation(Task):
    'Practical Task schema for desired search, observation, identification, classification, measurement, assessment, or monitoring'
    __occid_model_id__: ClassVar[int] = 312
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    intent: InformationIntent

class TaskTransport(Task):
    'Practical Task schema for desired movement of cargo, personnel, supplies, casualties, or recoverable assets'
    __occid_model_id__: ClassVar[int] = 313
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    intent: TransportIntent
