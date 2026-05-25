"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class Struct_type(IntEnum):
    VECTOR = 0
    MEASUREMENT = auto()
    BEARING = auto()
    GEO_POS = auto()
    LOCAL_POS = auto()
    LINE = auto()
    PATH = auto()
    SHAPE = auto()
    BOUNDING = auto()
    UNCERTAINTY = auto()
    POSE = auto()
    RANGE = auto()
    TRANSFORM = auto()
    ORBITAL = auto()
    SPATIAL = auto()

### Models

class Struct(Root):
    pass

class Vector(Struct):
    pass

class Measurement(Struct):
    pass

class Bearing(Struct):
    pass

class GeoPos(Struct):
    pass

class LocalPos(Struct):
    pass

class Line(Struct):
    pass

class StructPath(Struct):
    pass

class Shape(Struct):
    pass

class Bounding(Struct):
    pass

class Uncertainty(Struct):
    pass

class Pose(Struct):
    pass

class Range(Struct):
    pass

class Transform(Struct):
    pass

class Orbital(Struct):
    pass

class Time(Measurement):
    utime: int

class Duration(Measurement):
    ms: float | None = None
    seconds: float | None = None
    minutes: float | None = None
    hours: float | None = None
    days: float | None = None
    weeks: float | None = None
    months: float | None = None
    years: float | None = None

class Timestamp(Measurement):
    ms: float
    seconds: float
    minutes: float
    hours: float
    day: float
    month: float
    year: float
    tz: float

class ItemCount(Measurement):
    item_type: str
    qty: int = 0

class NumericRange(Range):
    min_value: float | None = None
    max_value: float | None = None
