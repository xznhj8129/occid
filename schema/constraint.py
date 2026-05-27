"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Constraint_type(IntEnum):
    RESTRICTION = 0
    LIMITATION = auto()
    CONDITION = auto()

### Models

class Constraint(Control):
    'Limit, rule, condition, or time/resource bound applied to directed work'

class Restriction(Constraint):
    pass

class Limitation(Constraint):
    pass

class ConstraintCondition(Constraint):
    pass

class TaskTimeWindow(Constraint):
    earliest_start: float | None = None
    latest_finish: float | None = None
