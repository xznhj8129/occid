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
    MILITARY = auto()

class GroundMachine_type(IntEnum):
    MILITARY = 0

class AirMachine_type(IntEnum):
    MILITARY = 0

### Models

class Entity(Object):
    'One discrete "atom" capable of actions'
    entity_id: StringID
    short_id: StringID | None = None
    name: builtins.str | None = None
    entity_type: EntityType | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    created_ts: builtins.float | None = None
    updated_ts: builtins.float | None = None
    origin_system: builtins.str | None = None
    alt_ids: list[StringID]
    tags: list[builtins.str]
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[RelationSchema]
    location_state: LocationState | None = None
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None

class Actor(Entity):
    pass

class Agent(Actor):
    pass

class GroundNavigationSchema(Attribute):
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: builtins.float
    max_spd: builtins.float

class AirNavigationSchema(Attribute):
    flight_type: AirframeType
    control_modes: list[FlightMode]
    failsafe_mode: AirFailsafeMode | None = None
    weather_limits: WeatherLimits
    ifr: builtins.bool | None = None
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    fuel: FuelState | None = None
    max_range: builtins.float
    max_flight_t: builtins.float
    max_spd: builtins.float
    cruise_spd: builtins.float
    max_alt: builtins.float
    start_flight_time: builtins.float

class Person(Actor):
    entity_type: EntityType = EntityType.PERSON
    role: builtins.str
    serial_uid: StringID
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    health: HumanHealthStatus
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    links: dict[builtins.str, LinkSchema]

class Machine(Entity):
    entity_type: EntityType = EntityType.MACHINE
    sys_id: StringID
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
    model: builtins.str
    role: builtins.str
    serial_uid: StringID
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: GroundNavigationSchema

class AirMachine(Machine):
    machine_type: MachineType | None = None
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    serial_uid: StringID
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: AirNavigationSchema
    maint_status: MaintenanceStatus | None = None
