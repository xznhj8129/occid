"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Models

class Interface(Control):
    'Control surface, lease, operator input, remote-control mapping, or executor-facing command interface'

class ControlLease(Interface):
    asset_id: str
    holder_id: str
    control_level: ControlLevel
    lease_start: float
    lease_end: float
    lease_rev: int = 0
