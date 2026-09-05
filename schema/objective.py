"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .task import TaskPriority, TaskStatus

### Models

class SuccessCriterion(OCCIDModel):
    'Typed, human-readable condition used to determine whether an objective succeeded'
    __occid_model_id__: ClassVar[int] = 252
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    statement: builtins.str
    metric: builtins.str | None = None
    target_value: Semantic[MetadataValue] | None = None

class Objective(OCCIDModel):
    'Desired end state with intent, success rule, target, priority, and deadline'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Objective')]
    name: builtins.str
    intent: builtins.str
    desired_state: builtins.str
    success_criteria: list[Semantic[SuccessCriterion]]
    target_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    owner_uid: Semantic[UID] | None = None
    start_time: builtins.float | None = None
    deadline: builtins.float | None = None
