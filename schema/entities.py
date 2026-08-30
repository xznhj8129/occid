"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .attribute import Attribute
from .definition import OperationalDomain
from .object import Object

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

class Entity(Object):
    'One discrete "atom" capable of actions'
    __occid_model_id__: ClassVar[int] = 214
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    uid: UID
    id: builtins.int
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType | None = None
    tags: list[builtins.str]
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None

class Actor(Entity):
    __occid_model_id__: ClassVar[int] = 215
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Agent(Actor):
    __occid_model_id__: ClassVar[int] = 216
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class GroundNavigationSchema(Attribute):
    __occid_model_id__: ClassVar[int] = 217
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: builtins.float
    max_spd: builtins.float

class AirNavigationSchema(Attribute):
    __occid_model_id__: ClassVar[int] = 218
    __occid_semantic_role__: ClassVar[str] = 'specialization'
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

class Person(Actor):
    __occid_model_id__: ClassVar[int] = 219
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    entity_type: EntityType = EntityType.PERSON
    role: builtins.str
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]

class Machine(Entity):
    __occid_model_id__: ClassVar[int] = 220
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    entity_type: EntityType = EntityType.MACHINE
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]

class Vehicle(Machine):
    __occid_model_id__: ClassVar[int] = 221
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class Platform(Machine):
    __occid_model_id__: ClassVar[int] = 222
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class GroundMachine(Machine):
    __occid_model_id__: ClassVar[int] = 223
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    machine_type: MachineType
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: GroundNavigationSchema

class AirMachine(Machine):
    __occid_model_id__: ClassVar[int] = 224
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    airframe: AirframeType
    machine_type: MachineType | None = None
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: AirNavigationSchema
