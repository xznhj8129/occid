"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Enums

class AssignmentStatus(IntEnum):
    PROPOSED = 0
    ASSIGNED = auto()
    ACCEPTED = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    REJECTED = auto()
    CANCELLED = auto()

### Models

class Assignment(Control):
    'Explicit binding of a task to an assignee under stated authority and constraints'
    __occid_model_id__: ClassVar[int] = 130
    record: RecordMeta
    assignment_id: StringID
    task_id: StringID
    assignee_id: StringID
    plan_id: StringID | None = None
    authority_id: StringID | None = None
    assigned_by: StringID
    assigned_at: builtins.float
    accepted_at: builtins.float | None = None
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | ConstraintCondition | TaskTimeWindow | WeatherLimits]]

class FlightAssignment(Assignment):
    __occid_model_id__: ClassVar[int] = 132
    num: builtins.int
    unit_id: StringID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_time: builtins.float = 0.0
