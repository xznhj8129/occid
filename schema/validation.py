"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ValidationStatus(IntEnum):
    NOT_STARTED = 0
    RUNNING = auto()
    VALID = auto()
    FAILED = auto()

### Models

class Validation(OCCIDModel):
    'Mutable state of evaluating a Condition, kept separate from the predicate itself'
    __occid_model_id__: ClassVar[int] = 262
    __occid_semantic_role__: ClassVar[str] = 'type'
    condition: Predicate | BooleanLogic
    status: ValidationStatus
    updated_ts: builtins.float | None = None
