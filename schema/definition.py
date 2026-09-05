"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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

class Definition(OCCIDModel):
    'Abstract structure used to define how values, space, geometry, time, or relations are interpreted; semantic descriptors.'
    __occid_model_id__: ClassVar[int] = 55
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Frame', 'Coordinate', 'Geometry', 'DefinitionRelationship', 'SemanticType')

class Frame(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 90
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Coordinate(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 49
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Geometry(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 98
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class DefinitionRelationship(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 56
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class SemanticType(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 235
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Category', 'Role', 'Function', 'Domain')

class Category(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 28
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Role(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 228
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Function(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 93
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Domain(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 64
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
