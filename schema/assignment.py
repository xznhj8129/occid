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
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TaskAssignment', 'RoleAssignment', 'FlightAssignment')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: Semantic[UID]
    authority_uid: Semantic[UID]
    assigned_by_uid: Semantic[UID]
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Semantic[Constraint]]

class TaskAssignment(OCCIDModel):
    'Assignment of a Task to an assignee'
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Assignment'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: Semantic[UID]
    authority_uid: Semantic[UID]
    assigned_by_uid: Semantic[UID]
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Semantic[Constraint]]
    task_uid: Semantic[UID]

class RoleAssignment(OCCIDModel):
    'Assignment of an organizational Role to an actor'
    __occid_model_id__: ClassVar[int] = 229
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Assignment'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: Semantic[UID]
    authority_uid: Semantic[UID]
    assigned_by_uid: Semantic[UID]
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Semantic[Constraint]]
    organization_uid: Semantic[UID]
    role: Semantic[OrgRole]

class FlightAssignment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 83
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Assignment'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Assignment')]
    assignee_uid: Semantic[UID]
    authority_uid: Semantic[UID]
    assigned_by_uid: Semantic[UID]
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[Semantic[Constraint]]
    num: builtins.int
    unit_uid: Semantic[UID] | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_ts: Semantic[Timestamp] = 0.0
