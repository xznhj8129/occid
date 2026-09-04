"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ExecutionPhase(IntEnum):
    CREATED = 0
    QUEUED = auto()
    RUNNING = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CANCELLED = auto()

### Models

class Execution(OCCIDModel):
    'One execution attempt for an assignment, independently tracked across local and external executors'
    __occid_model_id__: ClassVar[int] = 70
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Execution')]
    assignment_uid: UID
    executor_uid: UID
    attempt: builtins.int = 0
    phase: ExecutionPhase = ExecutionPhase.CREATED
    progress: builtins.float | None = None
    started_at: Timestamp
    completed_at: Timestamp
    result: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    failure: builtins.str | None = None
    external_job_refs: list[builtins.str]
