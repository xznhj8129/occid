"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Models

class Interface(Control):
    'Control surface, lease, operator input, remote-control mapping, or executor-facing command interface'

class ControlLease(Interface):
    asset_id: StringID
    holder_id: StringID
    control_level: ControlLevel
    lease_start: builtins.float
    lease_end: builtins.float
    lease_rev: builtins.int = 0
