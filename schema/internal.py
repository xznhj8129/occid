"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Internal(OCCIDModel):
    'Diagnostic internals of a machine or system.'
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('RuntimeLoadState',)

class RuntimeLoadState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 232
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Internal'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    cpu_load: builtins.int | None = None
    cycle_time_us: builtins.int | None = None
