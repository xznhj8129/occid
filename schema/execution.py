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
    __occid_model_id__: ClassVar[int] = 79
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Execution')]
    assignment_uid: Semantic[UID]
    executor_uid: Semantic[UID]
    attempt: builtins.int = 0
    phase: ExecutionPhase = ExecutionPhase.CREATED
    progress: builtins.float | None = None
    started_at: Semantic[Timestamp]
    completed_at: Semantic[Timestamp]
    result: Semantic[MetadataValue] | None = None
    failure: builtins.str | None = None
    external_job_refs: list[builtins.str]
