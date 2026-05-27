"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

### Models

class Internal(State):
    'Diagnostic internals of a machine or system (CPU, memory, cycles, firmware, connectivity)'

class FirmwareInfo(Internal):
    name: str
    version: Version
    build: str | None = None

class RuntimeLoadState(Internal):
    cpu_load: int | None = None
    cycle_time_us: int | None = None
