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

### Models

class Definition(Root):
    'Abstract structure used to define how values, space, geometry, time, or relations are interpreted; semantic descriptors.'
    __occid_model_id__: ClassVar[int] = 5

class Frame(Definition):
    __occid_model_id__: ClassVar[int] = 6

class Coordinate(Definition):
    __occid_model_id__: ClassVar[int] = 7

class Geometry(Definition):
    __occid_model_id__: ClassVar[int] = 8

class DefinitionRelationship(Definition):
    __occid_model_id__: ClassVar[int] = 9

class SemanticType(Definition):
    __occid_model_id__: ClassVar[int] = 10

class Category(SemanticType):
    __occid_model_id__: ClassVar[int] = 11

class Role(SemanticType):
    __occid_model_id__: ClassVar[int] = 12

class Function(SemanticType):
    __occid_model_id__: ClassVar[int] = 13

class Domain(SemanticType):
    __occid_model_id__: ClassVar[int] = 14
