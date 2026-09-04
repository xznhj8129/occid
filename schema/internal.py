"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Internal(OCCIDModel):
    'Diagnostic internals of a machine or system.'
    __occid_model_id__: ClassVar[int] = 111
    __occid_semantic_role__: ClassVar[str] = 'type'

class RuntimeLoadState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 216
    __occid_semantic_role__: ClassVar[str] = 'representation'
    cpu_load: builtins.int | None = None
    cycle_time_us: builtins.int | None = None
