"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Internal(OCCIDModel):
    'Diagnostic internals of a machine or system.'
    __occid_model_id__: ClassVar[int] = 110
    __occid_semantic_role__: ClassVar[str] = 'type'

class FirmwareInfo(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 72
    __occid_semantic_role__: ClassVar[str] = 'representation'
    name: builtins.str
    version: Version
    build: builtins.str | None = None

class RuntimeLoadState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 213
    __occid_semantic_role__: ClassVar[str] = 'representation'
    cpu_load: builtins.int | None = None
    cycle_time_us: builtins.int | None = None
