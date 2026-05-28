"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .root import Root

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
    'Primitive reusable low-level struct families.'

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
    seconds: float | None = None
    minutes: int | None = None
    hours: int | None = None
    days: int | None = None
    weeks: int | None = None
    months: int | None = None
    years: int | None = None

class Timestamp(Measurement):
    seconds: float
    minutes: int
    hours: int
    day: int
    month: int
    year: int
    tz: int

class ItemCount(Measurement):
    item_type: str
    qty: int = 0

class NumericRange(Range):
    min_value: float | None = None
    max_value: float | None = None
