"""Generated from core/schemav2."""
from __future__ import annotations
from enum import IntEnum as _StdIntEnum, IntEnum, auto, Enum
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

SchemaVersion = tuple[int, int, int]

### Enums

class IntEnum(_StdIntEnum):
    @classmethod
    def _missing_(cls, value):
        if type(value) == str:
            return cls[value]
        return super()._missing_(value)

### Models

class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if type(value) == dict:
                return {key: encode(item) for key, item in value.items()}
            if type(value) in (list, tuple):
                return [encode(item) for item in value]
            if issubclass(type(value), IntEnum):
                return value.name
            if issubclass(type(value), Enum):
                return value.value
            return value

        if mode == "json":
            data = super().model_dump(mode="python", **kwargs)
            return encode(data)
        data = super().model_dump(mode=mode, **kwargs)
        return data

### Schema Enums

class ConfidenceLevel(IntEnum):
    UNKNOWN = 0
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CONFIRMED = auto()

class OperationalDomain(IntEnum):
    LAND = 0
    AIR = auto()
    SEA = auto()
    SUB = auto()
    SPACE = auto()
    CYBER = auto()
    ALL = auto()

class EffectDomain(IntEnum):
    LAND = 0
    AIR = auto()
    SEA = auto()
    SUB = auto()
    SPACE = auto()
    CYBER = auto()
    ALL = auto()

class SchemaKind(IntEnum):
    BASIC_UNIT = 0
    GROUND_ORG = auto()
    AIR_ORG = auto()
    AIR_UNIT = auto()
    GROUND_UNIT = auto()
    LINK = auto()
    SENSOR = auto()
    INSTALLATION = auto()

class PriorityLevel(IntEnum):
    LOW = 0
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

class PropulsionType(IntEnum):
    FOOT = 0
    WHEELED = auto()
    TRACKED = auto()
    ROTARY_WING = auto()
    FIXED_WING = auto()
    JET = auto()
    MARITIME = auto()
    STATIC = auto()

class NavigationMode(IntEnum):
    MANUAL = 0
    INS = auto()
    GNSS = auto()
    INS_GNSS = auto()
    VISUAL = auto()
    TERRAIN_FOLLOW = auto()

class FuelType(IntEnum):
    BATTERY = 0
    GASOLINE = auto()
    DIESEL = auto()
    HEAVY_FUEL = auto()
    JET_FUEL = auto()
    HYBRID = auto()

class Root_type(IntEnum):
    DEFINITION = 0
    STRUCT = auto()
    OBJECT = auto()
    CONTROL = auto()
    COMMUNICATION = auto()
    DATA = auto()

class Definition_type(IntEnum):
    FRAME = 0
    COORDINATE = auto()
    GEOMETRY = auto()
    SEMANTIC_TYPE = auto()
    RELATIONSHIP = auto()

class SemanticType_type(IntEnum):
    CATEGORY = 0
    ROLE = auto()
    FUNCTION = auto()
    FACTION_AXIS = auto()
    DOMAIN = auto()

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

### Schema Models

class Root(OCCIDModel):
    'Any distinct part of the overall framework that can be identified, described, or referenced'

class Definition(Root):
    'Abstract structure used to define how values, space, geometry, time, or relations are interpreted; semantic descriptors.'

class Frame(Definition):
    pass

class Coordinate(Definition):
    pass

class Geometry(Definition):
    pass

class SemanticType(Definition):
    pass

class Category(SemanticType):
    pass

class Role(SemanticType):
    pass

class Function(SemanticType):
    pass

class FactionAxis(SemanticType):
    pass

class Domain(SemanticType):
    pass

class DefinitionRelationship(Definition):
    pass

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
