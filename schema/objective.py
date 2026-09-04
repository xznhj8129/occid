"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .task import TaskPriority, TaskStatus

### Models

class Objective(OCCIDModel):
    'Desired end state with intent, success rule, target, priority, and deadline'
    __occid_model_id__: ClassVar[int] = 169
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Objective')]
    name: builtins.str
    intent: builtins.str
    desired_state: builtins.str
    success_criteria: list[SuccessCriterion]
    target_uids: list[UID]
    constraints: list[Constraint]
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    owner_uid: UID | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None

class SuccessCriterion(OCCIDModel):
    'Typed, human-readable condition used to determine whether an objective succeeded'
    __occid_model_id__: ClassVar[int] = 236
    __occid_semantic_role__: ClassVar[str] = 'representation'
    statement: builtins.str
    metric: builtins.str | None = None
    target_value: MetadataValue | None = None
