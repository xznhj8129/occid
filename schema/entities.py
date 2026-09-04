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

class Actor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 2
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None

class Machine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 133
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]

class Agent(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 3
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None

class Person(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 182
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.PERSON
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    role: builtins.str
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    sensors: dict[builtins.str, SensorPayload]

class Vehicle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 267
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]

class Platform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 188
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]

class GroundNavigation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 94
    __occid_semantic_role__: ClassVar[str] = 'representation'
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: builtins.float
    max_spd: builtins.float

class AirNavigation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 6
    __occid_semantic_role__: ClassVar[str] = 'representation'
    flight_type: AirframeType
    control_modes: list[StandardFlightMode]
    failsafe_mode: AirFailsafeMode | None = None
    weather_limits: WeatherLimits
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
    __occid_model_id__: ClassVar[int] = 93
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType
    components: list[EntityComponentRef]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, SensorPayload]
    navigation: GroundNavigation

class AirMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 5
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, SensorPayload]
    navigation: AirNavigation
