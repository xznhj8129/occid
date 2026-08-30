"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Enums

class ExecutionPhase(IntEnum):
    CREATED = 0
    QUEUED = auto()
    RUNNING = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CANCELLED = auto()

### Models

class Execution(State):
    'One execution attempt for an assignment, independently tracked across local and external executors'
    __occid_model_id__: ClassVar[int] = 281
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    uid: UID
    id: builtins.int
    assignment_uid: UID
    executor_uid: UID
    attempt: builtins.int = 0
    phase: ExecutionPhase = ExecutionPhase.CREATED
    progress: builtins.float | None = None
    started_at: builtins.float | None = None
    completed_at: builtins.float | None = None
    result: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    failure: builtins.str | None = None
    external_job_refs: list[builtins.str]

class ExecutionAcceptance(State):
    'Executor admission decision for one exact dispatch of an existing Execution; distinct from transport delivery and from execution completion'
    __occid_model_id__: ClassVar[int] = 298
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    execution_uid: UID
    dispatch_ref: builtins.str
    executor_uid: UID
    accepted: builtins.bool
    retryable: builtins.bool = False
    reason: builtins.str | None = None
    reported_at: builtins.float

class ExecutionStatusReport(State):
    'Executor report for one exact execution dispatch; may report that no retained status exists and is distinct from transport delivery evidence'
    __occid_model_id__: ClassVar[int] = 300
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    execution_uid: UID
    dispatch_ref: builtins.str
    executor_uid: UID
    found: builtins.bool = True
    phase: ExecutionPhase | None = None
    progress: builtins.float | None = None
    task_delta: TaskDelta | None = None
    entity_state: EntityState | None = None
    failure: builtins.str | None = None
    reported_at: builtins.float

class TaskDelta(State):
    'Time-indexed task-state update; not an assignment definition'
    __occid_model_id__: ClassVar[int] = 131
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    task_uid: UID
    task_rev: builtins.int = 0
    phase: TaskPhase
    progress: builtins.float | None = None
    owner_uid: UID | None = None
    updated_ts: builtins.float
