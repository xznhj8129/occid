"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Directive_type(IntEnum):
    MISSION = 0
    TASK = auto()
    COMMAND = auto()

### Models

class Directive(Control):
    'What must be achieved, why, and within what bounds'

class Mission(Directive):
    pass

class Command(Directive):
    pass

class MissionProgress(Mission):
    waypoint_count: int | None = None
    current_waypoint_index: int | None = None
    mission_valid: bool | None = None
