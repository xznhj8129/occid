"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Models

class Struct(Root):
    'Primitive reusable low-level struct families.'
    __occid_model_id__: ClassVar[int] = 25
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Vector(Struct):
    __occid_model_id__: ClassVar[int] = 26
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Measurement(Struct):
    __occid_model_id__: ClassVar[int] = 27
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Bearing(Struct):
    __occid_model_id__: ClassVar[int] = 28
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class GeoPos(Struct):
    __occid_model_id__: ClassVar[int] = 29
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class LocalPos(Struct):
    __occid_model_id__: ClassVar[int] = 30
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Line(Struct):
    __occid_model_id__: ClassVar[int] = 31
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class StructPath(Struct):
    __occid_model_id__: ClassVar[int] = 32
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Shape(Struct):
    __occid_model_id__: ClassVar[int] = 33
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Bounding(Struct):
    __occid_model_id__: ClassVar[int] = 34
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Uncertainty(Struct):
    __occid_model_id__: ClassVar[int] = 35
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Pose(Struct):
    __occid_model_id__: ClassVar[int] = 36
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Range(Struct):
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Transform(Struct):
    __occid_model_id__: ClassVar[int] = 38
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Orbital(Struct):
    __occid_model_id__: ClassVar[int] = 39
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Time(Measurement):
    __occid_model_id__: ClassVar[int] = 40
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    utime: builtins.int

class Duration(Measurement):
    __occid_model_id__: ClassVar[int] = 41
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(Measurement):
    __occid_model_id__: ClassVar[int] = 42
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    seconds: builtins.float
    minutes: builtins.int
    hours: builtins.int
    day: builtins.int
    month: builtins.int
    year: builtins.int
    tz: builtins.int

class ItemCount(Measurement):
    __occid_model_id__: ClassVar[int] = 43
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(Range):
    __occid_model_id__: ClassVar[int] = 44
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
