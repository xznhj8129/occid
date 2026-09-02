"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ActivationPhase(IntEnum):
    STANDBY = 0
    VALIDATING = auto()
    READY = auto()
    ENABLED = auto()
    EXECUTING = auto()
    EXHAUSTED = auto()

### Models

class Activation(OCCIDModel):
    'Mutable lifecycle of an activatable object or capability; faults remain orthogonal Health state'
    __occid_model_id__: ClassVar[int] = 1
    __occid_semantic_role__: ClassVar[str] = 'type'
    phase: ActivationPhase
    remaining_uses: builtins.int | None = None
