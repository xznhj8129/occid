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
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    assignment_id: UID
    task_id: UID
    assignee_id: UID
    plan_id: UID | None = None
    authority_id: UID | None = None
    assigned_by: UID
    assigned_at: builtins.float
    accepted_at: builtins.float | None = None
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]

class FlightAssignment(Assignment):
    __occid_model_id__: ClassVar[int] = 132
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    num: builtins.int
    unit_id: UID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_time: builtins.float = 0.0
