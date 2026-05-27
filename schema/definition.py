"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

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

### Models

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
