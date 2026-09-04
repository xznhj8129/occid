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
    'Deliberate binding of an assignee to a subject under stated authority and constraints'
    __occid_model_id__: ClassVar[int] = 13
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: UID
    authority_uid: UID
    assigned_by_uid: UID
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]

class TaskAssignment(OCCIDModel):
    'Assignment of a Task to an assignee'
    __occid_model_id__: ClassVar[int] = 244
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: UID
    authority_uid: UID
    assigned_by_uid: UID
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]
    task_uid: UID

class RoleAssignment(OCCIDModel):
    'Assignment of an organizational Role to an actor'
    __occid_model_id__: ClassVar[int] = 214
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: UID
    authority_uid: UID
    assigned_by_uid: UID
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]
    organization_uid: UID
    role: OrgRole

class FlightAssignment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 74
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: UID
    authority_uid: UID
    assigned_by_uid: UID
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Constraint]
    num: builtins.int
    unit_uid: UID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_ts: Timestamp = 0.0
