"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class DirectiveType(IntEnum):
    MISSION = 0
    TASK = auto()
    COMMAND = auto()

### Models

class Directive(Control):
    pass

class Mission(Directive):
    pass

class Task(Directive):
    pass

class Command(Directive):
    pass
