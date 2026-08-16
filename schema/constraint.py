"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Models

class Constraint(Control):
    'Limit, rule, or time/resource bound applied to directed work'
    __occid_model_id__: ClassVar[int] = 60
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    condition: SerializeAsAny[Condition | Predicate | BooleanLogic] | None = None

class Restriction(Constraint):
    __occid_model_id__: ClassVar[int] = 61
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Limitation(Constraint):
    __occid_model_id__: ClassVar[int] = 62
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class TaskTimeWindow(Constraint):
    __occid_model_id__: ClassVar[int] = 64
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    earliest_start: builtins.float | None = None
    latest_finish: builtins.float | None = None

class WeatherLimits(Constraint):
    __occid_model_id__: ClassVar[int] = 65
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    ifr: builtins.bool | None = None
    night: builtins.bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: builtins.bool | None = None
