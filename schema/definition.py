"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

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

class AlternateIdType(IntEnum):
    TRACK_ID = 0
    ASSET_ID = auto()
    CALLSIGN = auto()
    SERIAL_NUMBER = auto()
    REGISTRATION = auto()
    UNIT_CODE = auto()
    TRACK_NUMBER = auto()
    JU_NUMBER = auto()

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
    GASOLINE = 0
    DIESEL = auto()
    HEAVY_FUEL = auto()
    JET_FUEL = auto()
    BATTERY = auto()
    HYBRID = auto()
