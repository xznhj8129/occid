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

class Reality(IntEnum):
    REAL = 0
    SIMULATED = auto()
    EXERCISE = auto()

### Models

class Definition(OCCIDModel):
    'Abstract structure used to define how values, space, geometry, time, or relations are interpreted; semantic descriptors.'
    __occid_model_id__: ClassVar[int] = 80
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Frame', 'Coordinate', 'Geometry', 'DefinitionRelationship', 'SemanticType', 'OrgTemplate', 'ResourceTemplate')

class Frame(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 128
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Coordinate(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 72
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Geometry(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 143
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class DefinitionRelationship(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 81
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class SemanticType(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 336
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Category', 'Role', 'Function', 'Domain')

class Category(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 45
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Role(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 325
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Function(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 132
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Domain(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 93
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SemanticType'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
