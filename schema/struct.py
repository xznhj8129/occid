"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Models

class Struct(Root):
    'Primitive reusable low-level struct families.'
    __occid_model_id__: ClassVar[int] = 25

class Vector(Struct):
    __occid_model_id__: ClassVar[int] = 26

class Measurement(Struct):
    __occid_model_id__: ClassVar[int] = 27

class Bearing(Struct):
    __occid_model_id__: ClassVar[int] = 28

class GeoPos(Struct):
    __occid_model_id__: ClassVar[int] = 29

class LocalPos(Struct):
    __occid_model_id__: ClassVar[int] = 30

class Line(Struct):
    __occid_model_id__: ClassVar[int] = 31

class StructPath(Struct):
    __occid_model_id__: ClassVar[int] = 32

class Shape(Struct):
    __occid_model_id__: ClassVar[int] = 33

class Bounding(Struct):
    __occid_model_id__: ClassVar[int] = 34

class Uncertainty(Struct):
    __occid_model_id__: ClassVar[int] = 35

class Pose(Struct):
    __occid_model_id__: ClassVar[int] = 36

class Range(Struct):
    __occid_model_id__: ClassVar[int] = 37

class Transform(Struct):
    __occid_model_id__: ClassVar[int] = 38

class Orbital(Struct):
    __occid_model_id__: ClassVar[int] = 39

class Time(Measurement):
    __occid_model_id__: ClassVar[int] = 40
    utime: builtins.int

class Duration(Measurement):
    __occid_model_id__: ClassVar[int] = 41
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(Measurement):
    __occid_model_id__: ClassVar[int] = 42
    seconds: builtins.float
    minutes: builtins.int
    hours: builtins.int
    day: builtins.int
    month: builtins.int
    year: builtins.int
    tz: builtins.int

class ItemCount(Measurement):
    __occid_model_id__: ClassVar[int] = 43
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(Range):
    __occid_model_id__: ClassVar[int] = 44
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
