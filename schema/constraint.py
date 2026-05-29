"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Models

class Constraint(Control):
    'Limit, rule, condition, or time/resource bound applied to directed work'
    __occid_model_id__: ClassVar[int] = 60

class Restriction(Constraint):
    __occid_model_id__: ClassVar[int] = 61

class Limitation(Constraint):
    __occid_model_id__: ClassVar[int] = 62

class ConstraintCondition(Constraint):
    __occid_model_id__: ClassVar[int] = 63

class TaskTimeWindow(Constraint):
    __occid_model_id__: ClassVar[int] = 64
    earliest_start: builtins.float | None = None
    latest_finish: builtins.float | None = None

class WeatherLimits(Constraint):
    __occid_model_id__: ClassVar[int] = 65
    ifr: builtins.bool | None = None
    night: builtins.bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: builtins.bool | None = None
