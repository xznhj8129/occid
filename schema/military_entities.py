"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .entities import AirMachine, GroundMachine, Machine, Person

### Models

class MilitaryPerson(Person):
    __occid_model_id__: ClassVar[int] = 274
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    attack_modes: list[AttackMode]
    weapons: list[ItemCount]
    ammo: list[ItemCount]

class MilitaryMachine(Machine):
    __occid_model_id__: ClassVar[int] = 275
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(GroundMachine):
    __occid_model_id__: ClassVar[int] = 276
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    payload: PayloadSchema
    effects: GroundEffectsSchema

class MilitaryAirMachine(AirMachine):
    __occid_model_id__: ClassVar[int] = 277
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    payload: PayloadSchema
    effects: AirEffectsSchema
