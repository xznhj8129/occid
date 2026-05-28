"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .object import Object, ObjectType
from .property import Attributes
from .root import OperationalDomain, PropulsionType

### Enums

class EntityType(IntEnum):
    PERSON = 0
    MACHINE = auto()
    SYSTEM = auto()

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

class Entity_type(IntEnum):
    ACTOR = 0
    MACHINE = auto()

class Actor_type(IntEnum):
    PERSON = 0
    AGENT = auto()

class AirNavigationSchema_type(IntEnum):
    MILITARY_AIR_NAVIGATION = 0

class Person_type(IntEnum):
    MILITARY = 0

class Machine_type(IntEnum):
    VEHICLE = 0
    ROBOT = auto()
    PLATFORM = auto()
    GROUND = auto()
    AIR = auto()
    MILITARY = auto()

class GroundMachine_type(IntEnum):
    GROUND_ROBOT = 0
    MILITARY = auto()

class AirMachine_type(IntEnum):
    AIR_ROBOT = 0
    MILITARY = auto()

### Models

class Entity(Object):
    'One discrete "atom" capable of actions'
    object_type: ObjectType = ObjectType.ENTITY
    entity_id: str
    short_id: str | None = None
    name: str | None = None
    entity_type: EntityType | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    created_ts: float | None = None
    updated_ts: float | None = None
    origin_system: str | None = None
    alt_ids: list[Identifier]
    tags: list[str]
    metadata: list[MetadataEntry]
    relations: list[RelationSchema]
    location_state: LocationState | None = None
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None

class Actor(Entity):
    pass

class Agent(Actor):
    pass

class GroundNavigationSchema(Attributes):
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: float
    max_spd: float

class AirNavigationSchema(Attributes):
    flight_type: AirframeType
    control_modes: list[FlightMode]
    failsafe_mode: AirFailsafeMode | None = None
    weather_limits: WeatherLimits
    ifr: bool | None = None
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    fuel: FuelState | None = None
    max_range: float
    max_flight_t: float
    max_spd: float
    cruise_spd: float
    max_alt: float
    start_flight_time: float

class Person(Actor):
    entity_type: EntityType = EntityType.PERSON
    role: str
    serial_uid: str = ''
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    health: HumanHealthStatus
    sensors: dict[str, SensorSchema]
    links: dict[str, LinkSchema]

class Machine(Entity):
    entity_type: EntityType = EntityType.MACHINE
    sys_id: str
    machine_type: MachineType | None = None
    status: EntityOperationalState
    health_snapshot: HealthSnapshot | None = None
    power_state: PowerStateSchema | None = None
    supplies: SuppliesSchema | None = None
    link_condition: LinkCondition | None = None
    control_level: ControlLevel | None = None
    components: list[EntityComponentRef]

class Vehicle(Machine):
    pass

class Platform(Machine):
    pass

class GroundMachine(Machine):
    machine_type: MachineType
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: str
    role: str
    serial_uid: str = ''
    sensors: dict[str, SensorSchema]
    navigation: GroundNavigationSchema

class AirMachine(Machine):
    machine_type: MachineType | None = None
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: str
    serial_uid: str = ''
    sensors: dict[str, SensorSchema]
    navigation: AirNavigationSchema
    maint_status: MaintenanceStatus | None = None
