"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .entities import AirMachine, GroundMachine, Machine, Person

### Models

class MilitaryPerson(Person):
    __occid_model_id__: ClassVar[int] = 269
    attack_modes: list[AttackMode]
    weapons: list[ItemCount]
    ammo: list[ItemCount]

class MilitaryMachine(Machine):
    __occid_model_id__: ClassVar[int] = 270
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(GroundMachine):
    __occid_model_id__: ClassVar[int] = 271
    payload: PayloadSchema
    effects: GroundEffectsSchema

class MilitaryAirMachine(AirMachine):
    __occid_model_id__: ClassVar[int] = 272
    payload: PayloadSchema
    effects: AirEffectsSchema
