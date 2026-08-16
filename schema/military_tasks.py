"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .struct import Struct

### Enums

class TaskCombat(IntEnum):
    DEFEND = 0
    ATTACK = auto()
    PROTECT = auto()
    COMBAT_SUPPORT = auto()
    COMBAT_RESERVE = auto()

### Models

class MunitionAllocation(Struct):
    __occid_model_id__: ClassVar[int] = 278
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    munition_type: builtins.str
    qty: builtins.int = 0

class CombatTaskProfile(Struct):
    'Military domain detail associated with a generic Task without creating a Task subtype'
    __occid_model_id__: ClassVar[int] = 309
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    task_id: StringID
    combat_task: TaskCombat | None = None
    target_category: TargetCategory | None = None
    target_point: GlobalPosition | None = None
    munitions: list[MunitionAllocation]
    effect: builtins.str | None = None
    desired_bda: builtins.bool = False
