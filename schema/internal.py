"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Internal(State):
    'Diagnostic internals of a machine or system.'
    __occid_model_id__: ClassVar[int] = 157
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class FirmwareInfo(Internal):
    __occid_model_id__: ClassVar[int] = 158
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    name: builtins.str
    version: Version
    build: builtins.str | None = None

class RuntimeLoadState(Internal):
    __occid_model_id__: ClassVar[int] = 159
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    cpu_load: builtins.int | None = None
    cycle_time_us: builtins.int | None = None
