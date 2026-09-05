"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain

### Enums

class EntityType(IntEnum):
    PERSON = 0
    MACHINE = auto()
    SYSTEM = auto()

class EntitySubtype(IntEnum):
    PERSON = 0
    PLATFORM = auto()
    VEHICLE = auto()
    GROUND_ROBOT = auto()
    AIR_ROBOT = auto()
    SURFACE_ROBOT = auto()

class MachineType(IntEnum):
    VEHICLE = 0
    ROBOT = auto()

class SystemType(IntEnum):
    PLATFORM = 0
    EQUIPMENT = auto()

class EntityOperationalState(IntEnum):
    UNKNOWN = 0
    READY = auto()
    ACTIVE = auto()
    DEGRADED = auto()
    MAINTENANCE = auto()
    DAMAGED = auto()
    DESTROYED = auto()
    OFFLINE = auto()

class EntityLifecycleStatus(IntEnum):
    ACTIVE = 0
    INACTIVE = auto()
    UNKNOWN = auto()

class AirframeType(IntEnum):
    FIXED_WING = 0
    COPTER = auto()
    VTOL = auto()
    TAILSITTER = auto()
    FLYING_WING = auto()

class CopterType(IntEnum):
    X = 0
    Y = auto()
    HEXA = auto()
    OCTO = auto()
    DECA = auto()
    HELICOPTER = auto()

class VTOLType(IntEnum):
    NONE = 0
    QUADPLANE = auto()
    TILT = auto()
    VECTORING = auto()
    TAILSITTER = auto()

class NavAids(IntEnum):
    NONE = 0
    GNSS = auto()
    INS = auto()
    TERRAIN_MATCH = auto()
    CELESTIAL = auto()
    VISUAL = auto()

class PropulsionType(IntEnum):
    FOOT = 0
    WHEELED = auto()
    TRACKED = auto()
    ROTARY_WING = auto()
    FIXED_WING = auto()
    JET = auto()
    MARITIME = auto()
    STATIC = auto()

### Models

class Entity(OCCIDModel):
    'One discrete "atom" capable of actions'
    __occid_model_id__: ClassVar[int] = 71
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Object'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Actor', 'Machine')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None

class Actor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 2
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Entity'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Agent', 'Person')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None

class Agent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 3
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Actor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None

class Person(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 196
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Actor'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryPerson',)
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.PERSON
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    role: builtins.str
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    sensors: dict[builtins.str, Semantic[SensorPayload]]

class Machine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 143
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Entity'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Vehicle', 'Platform', 'GroundMachine', 'AirMachine', 'Robot', 'MilitaryMachine')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]

class Vehicle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 285
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]

class Platform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 202
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]

class GroundNavigation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 103
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: builtins.float
    max_spd: builtins.float

class AirNavigation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 6
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryAirNavigation',)
    flight_type: AirframeType
    control_modes: list[StandardFlightMode]
    failsafe_mode: AirFailsafeMode | None = None
    weather_limits: Semantic[WeatherLimits]
    ifr: builtins.bool | None = None
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: builtins.float
    max_flight_t: builtins.float
    max_spd: builtins.float
    cruise_spd: builtins.float
    max_alt: builtins.float

class GroundMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GroundRobot', 'MilitaryGroundMachine')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType
    components: list[Semantic[EntityComponentRef]]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[GroundNavigation]

class AirMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 5
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AirRobot', 'MilitaryAirMachine')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[AirNavigation]
