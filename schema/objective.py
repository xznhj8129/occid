"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Objective_type(IntEnum):
    PURPOSE = 0
    INTENT = auto()

### Models

class Objective(Control):
    'Desired end state with intent, success rule, target, priority, and deadline'

class Purpose(Objective):
    pass

class Intent(Objective):
    pass

class ObjectiveSchema(Objective):
    objective_id: str
    intent: str
    success_rule: str | None = None
    priority: TaskPriority | None = None
    target_ref: str | None = None
    geo_goal: GlobalPosition | None = None
    end_condition: str | None = None
    deadline_ts: float | None = None

class ObjectiveBinding(Objective):
    objective_id: str
    task_ids: list[str]
    priority: TaskPriority | None = None
    deadline_ts: float | None = None
    success_rule: str | None = None
