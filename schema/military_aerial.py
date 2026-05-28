"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .entities import AirNavigationSchema
from .plan import UnitFlightPlan
from .reference import MissionPoi

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

AIR_ROLE_LABELS: dict[AirRole, str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

AIR_ROLE_NAMES: dict[AirRole, str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

### Models

class MilitaryAirNavigation(AirNavigationSchema):
    roles: list[AirRole]

class MilitaryMissionPoi(MissionPoi):
    sidc: int | None = None

class MilitaryUnitFlightPlan(UnitFlightPlan):
    target: PlannerMissionPoint
