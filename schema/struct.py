"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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
    utime: builtins.int

class Duration(Measurement):
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(Measurement):
    seconds: builtins.float
    minutes: builtins.int
    hours: builtins.int
    day: builtins.int
    month: builtins.int
    year: builtins.int
    tz: builtins.int

class ItemCount(Measurement):
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(Range):
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
