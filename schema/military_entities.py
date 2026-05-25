"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .entities import AirMachine, BaseMachine, GroundMachine, Person

### Models

class MilitaryPerson(Person):
    attack_modes: list[AttackMode]
    weapons: list[ItemCount]
    ammo: list[ItemCount]

class MilitaryMachine(BaseMachine):
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(GroundMachine):
    payload: PayloadSchema
    effects: GroundEffectsSchema

class MilitaryAirMachine(AirMachine):
    payload: PayloadSchema
    effects: AirEffectsSchema
