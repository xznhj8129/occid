"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class Assignment(OCCIDModel):
    'Explicit binding of a task to an assignee under stated authority and constraints'
    __occid_model_id__: ClassVar[int] = 13
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    task_uid: UID
    assignee_uid: UID
    plan_uid: UID | None = None
    authority_uid: UID | None = None
    assigned_by_uid: UID
    assigned_at: builtins.float
    accepted_at: builtins.float | None = None
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]

class FlightAssignment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 73
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    task_uid: UID
    assignee_uid: UID
    plan_uid: UID | None = None
    authority_uid: UID | None = None
    assigned_by_uid: UID
    assigned_at: builtins.float
    accepted_at: builtins.float | None = None
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]
    num: builtins.int
    unit_uid: UID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_time: builtins.float = 0.0
