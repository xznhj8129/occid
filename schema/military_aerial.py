"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .plan import PlanApprovalState

### Enums

class MilitaryAirTask(IntEnum):
    ISR = 0
    CLOSE_AIR_SUPPORT = auto()
    ELECTRONIC_WARFARE = auto()
    STRIKE = auto()
    SEAD = auto()

class AirRole(IntEnum):
    GROUND = 0
    AIR_DEFENSE = auto()
    FIGHTER = auto()
    GROUND_ATTACK = auto()
    ISR = auto()
    MINE = auto()
    CARGO = auto()

class AirCombatTask(IntEnum):
    STRIKE = 0
    CAS = auto()
    CAP = auto()
    INTERCEPT = auto()
    HK = auto()

class AirISRType(IntEnum):
    OVERFLY = 0
    FLYBY = auto()
    ORBIT = auto()

class AirAttackMode(IntEnum):
    ONEWAY = 0
    DROPPER = auto()
    DIVE = auto()
    STRAFE = auto()
    STANDOFF_LAUNCH = auto()

### Mappings

AIR_ROLE_LABELS: dict[AirRole, builtins.str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

AIR_ROLE_NAMES: dict[AirRole, builtins.str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

### Models

class MilitaryAirNavigation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 149
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
    roles: list[AirRole]

class MilitaryUnitFlightPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 155
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Plan')]
    name: builtins.str | None = None
    objective_uids: list[UID]
    task_uids: list[UID]
    actor_uids: list[UID]
    resource_uids: list[UID]
    assignment_uids: list[UID]
    steps: list[PlanStep]
    routes: list[GeoPath]
    constraints: list[Constraint]
    contingencies: list[PlanContingency]
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    unit_num: builtins.int
    callsign: builtins.str
    fl: builtins.float
    route_in: GeoPath
    target: PlannerMissionPoint
    route_out: GeoPath
    home: GlobalPosition
    land_pos: GlobalPosition
    ip_wait_delay: builtins.float = 0.0
    wp: GeoPath
