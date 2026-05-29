"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Internal(State):
    'Diagnostic internals of a machine or system.'
    __occid_model_id__: ClassVar[int] = 154

class FirmwareInfo(Internal):
    __occid_model_id__: ClassVar[int] = 155
    name: builtins.str
    version: Version
    build: builtins.str | None = None

class RuntimeLoadState(Internal):
    __occid_model_id__: ClassVar[int] = 156
    cpu_load: builtins.int | None = None
    cycle_time_us: builtins.int | None = None
