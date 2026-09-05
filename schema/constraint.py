"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Constraint(OCCIDModel):
    'Limit, rule, or time/resource bound applied to directed work'
    __occid_model_id__: ClassVar[int] = 42
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Restriction', 'Limitation', 'TaskTimeWindow', 'WeatherLimits')
    condition: Semantic[Condition] | None = None

class Restriction(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 225
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Constraint'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition] | None = None

class Limitation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 129
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Constraint'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition] | None = None

class TaskTimeWindow(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 267
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Constraint'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition] | None = None
    earliest_start: builtins.float | None = None
    latest_finish: builtins.float | None = None

class WeatherLimits(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 292
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Constraint'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition] | None = None
    ifr: builtins.bool | None = None
    night: builtins.bool | None = None
    rain: Semantic[NumericRange] | None = None
    snow: Semantic[NumericRange] | None = None
    temp: Semantic[NumericRange] | None = None
    wind: Semantic[NumericRange] | None = None
    vis: Semantic[NumericRange] | None = None
    icing: builtins.bool | None = None
