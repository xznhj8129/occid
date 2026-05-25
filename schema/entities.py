"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .definition import OperationalDomain, PropulsionType
from .objects import BaseObject, ObjectType

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

class BaseEntityType(IntEnum):
    PERSON = 0
    MACHINE = auto()

class BaseMachineType(IntEnum):
    GROUND = 0
    AIR = auto()

class GroundMachineType(IntEnum):
    GROUND_ROBOT = 0

class AirMachineType(IntEnum):
    AIR_ROBOT = 0

### Models

class BaseEntity(BaseObject):
    object_type: ObjectType = ObjectType.ENTITY
    entity_id: str
    short_id: str | None = None
    name: str | None = None
    entity_type: EntityType | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    created_ts: float | None = None
    updated_ts: float | None = None
    origin_system: str | None = None
    alt_ids: list[AlternateId]
    tags: list[str]
    metadata: list[MetadataEntry]
    relations: list[RelationSchema]
    location_state: LocationState | None = None
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None

class EntityComponentRef(OCCIDModel):
    component_id: str
    component_type: str | None = None
    label: str | None = None

class Person(BaseEntity):
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

class BaseMachine(BaseEntity):
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

class GroundNavigationSchema(OCCIDModel):
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: float
    max_spd: float

class AirNavigationSchema(OCCIDModel):
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

class GroundMachine(BaseMachine):
    machine_type: MachineType
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: str
    role: str
    serial_uid: str = ''
    sensors: dict[str, SensorSchema]
    navigation: GroundNavigationSchema

class GroundRobot(GroundMachine):
    machine_type: MachineType = MachineType.ROBOT
    robot_control: RobotControlSchema | None = None
    remote_control: RemoteControlSchema

class AirMachine(BaseMachine):
    machine_type: MachineType | None = None
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: str
    serial_uid: str = ''
    sensors: dict[str, SensorSchema]
    navigation: AirNavigationSchema
    maint_status: MaintenanceStatus | None = None

class AirRobot(AirMachine):
    machine_type: MachineType = MachineType.ROBOT
    robot_control: RobotControlSchema | None = None
    remote_control: RemoteControlSchema
