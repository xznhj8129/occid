"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .entity import AirMachine, GroundMachine, Machine, Person

### Models

class MilitaryPerson(Person):
    attack_modes: list[AttackMode]
    weapons: list[ItemCount]
    ammo: list[ItemCount]

class MilitaryMachine(Machine):
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(GroundMachine):
    payload: PayloadSchema
    effects: GroundEffectsSchema

class MilitaryAirMachine(AirMachine):
    payload: PayloadSchema
    effects: AirEffectsSchema
