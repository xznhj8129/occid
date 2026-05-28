"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

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

class ClassificationLevel(IntEnum):
    UNCLASSIFIED = 0
    CONTROLLED = auto()
    CONFIDENTIAL = auto()
    SECRET = auto()
    TOP_SECRET = auto()

class MediaType(IntEnum):
    IMAGE = 0
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    BINARY = auto()

class PowerStatus(IntEnum):
    UNKNOWN = 0
    NOT_PRESENT = auto()
    OPERATING = auto()
    DISABLED = auto()
    ERROR = auto()

class PowerType(IntEnum):
    UNKNOWN = 0
    GAS = auto()
    BATTERY = auto()
    SOLAR = auto()
    NUCLEAR = auto()

class Faction(IntEnum):
    UNKNOWN = 0
    PENDING = auto()
    FRIENDLY = auto()
    SUSPECT = auto()
    HOSTILE = auto()
    NEUTRAL = auto()
    ASSUMED = auto()
    FAKER = auto()
    JOKER = auto()

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

class DefinitionRelationship(Definition):
    pass

class SemanticType(Definition):
    pass

class Category(SemanticType):
    pass

class Role(SemanticType):
    pass

class Function(SemanticType):
    pass

class Domain(SemanticType):
    pass
