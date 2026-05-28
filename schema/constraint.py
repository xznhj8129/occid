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

class WeatherLimits(Constraint):
    ifr: bool | None = None
    night: bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: bool | None = None
