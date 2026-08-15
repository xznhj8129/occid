"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Enums

class ValidationStatus(IntEnum):
    NOT_STARTED = 0
    RUNNING = auto()
    VALID = auto()
    FAILED = auto()

### Models

class Validation(State):
    'Mutable state of evaluating a Condition, kept separate from the predicate itself'
    __occid_model_id__: ClassVar[int] = 321
    condition: SerializeAsAny[Condition | Predicate | BooleanLogic]
    status: ValidationStatus
    updated_ts: builtins.float | None = None
