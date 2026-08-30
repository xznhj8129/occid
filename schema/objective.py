"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control
from .struct import Struct
from .task import TaskPriority, TaskStatus

### Models

class SuccessCriterion(Struct):
    'Typed, human-readable condition used to determine whether an objective succeeded'
    __occid_model_id__: ClassVar[int] = 285
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    criterion_id: builtins.int
    statement: builtins.str
    metric: builtins.str | None = None
    target_value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None

class Objective(Control):
    'Desired end state with intent, success rule, target, priority, and deadline'
    __occid_model_id__: ClassVar[int] = 84
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    objective_id: UID
    name: builtins.str
    intent: builtins.str
    desired_state: builtins.str
    success_criteria: list[SuccessCriterion]
    target_refs: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    owner_id: UID | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
