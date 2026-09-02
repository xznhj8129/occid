"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Constraint(OCCIDModel):
    'Limit, rule, or time/resource bound applied to directed work'
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'type'
    condition: (Predicate | BooleanLogic) | None = None

class Restriction(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 209
    __occid_semantic_role__: ClassVar[str] = 'representation'
    condition: (Predicate | BooleanLogic) | None = None

class Limitation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'representation'
    condition: (Predicate | BooleanLogic) | None = None

class TaskTimeWindow(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'representation'
    condition: (Predicate | BooleanLogic) | None = None
    earliest_start: builtins.float | None = None
    latest_finish: builtins.float | None = None

class WeatherLimits(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 271
    __occid_semantic_role__: ClassVar[str] = 'representation'
    condition: (Predicate | BooleanLogic) | None = None
    ifr: builtins.bool | None = None
    night: builtins.bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: builtins.bool | None = None
