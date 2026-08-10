"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Enums

class AssignmentStatus(IntEnum):
    PROPOSED = 0
    ASSIGNED = auto()
    ACCEPTED = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    REJECTED = auto()
    CANCELLED = auto()

class ExecutionPhase(IntEnum):
    CREATED = 0
    QUEUED = auto()
    RUNNING = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CANCELLED = auto()

### Models

class Assignment(State):
    'Explicit binding of a task to an assignee under stated authority and constraints'
    __occid_model_id__: ClassVar[int] = 130
    record: RecordMeta
    assignment_id: StringID
    task_id: StringID
    assignee_id: StringID
    plan_id: StringID | None = None
    authority: builtins.str
    assigned_by: StringID
    assigned_at: builtins.float
    accepted_at: builtins.float | None = None
    status: AssignmentStatus = AssignmentStatus.PROPOSED
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | ConstraintCondition | TaskTimeWindow | WeatherLimits]]

class Execution(State):
    'One execution attempt for an assignment, independently tracked across local and external executors'
    __occid_model_id__: ClassVar[int] = 281
    record: RecordMeta
    execution_id: StringID
    assignment_id: StringID
    executor_id: StringID
    attempt: builtins.int = 0
    phase: ExecutionPhase = ExecutionPhase.CREATED
    progress: builtins.float | None = None
    started_at: builtins.float | None = None
    completed_at: builtins.float | None = None
    result: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    failure: builtins.str | None = None
    external_job_refs: list[StringID]

class ExecutionAcceptance(State):
    'Executor admission decision for one exact dispatch of an existing Execution; distinct from transport delivery and from execution completion'
    __occid_model_id__: ClassVar[int] = 298
    execution_id: StringID
    dispatch_id: StringID
    executor_id: StringID
    accepted: builtins.bool
    retryable: builtins.bool = False
    reason: builtins.str | None = None
    reported_at: builtins.float

class TaskDelta(State):
    'Time-indexed task-state update; not an assignment definition'
    __occid_model_id__: ClassVar[int] = 131
    record: RecordMeta
    task_id: StringID
    task_rev: builtins.int = 0
    phase: TaskPhase
    progress: builtins.float | None = None
    owner_id: StringID | None = None
    updated_ts: builtins.float

class FlightAssignment(Assignment):
    __occid_model_id__: ClassVar[int] = 132
    num: builtins.int
    unit_id: StringID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_time: builtins.float = 0.0
