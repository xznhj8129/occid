"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .directive import Task

### Enums

class TaskCombat(IntEnum):
    DEFEND = 0
    ATTACK = auto()
    PROTECT = auto()
    COMBAT_SUPPORT = auto()
    COMBAT_RESERVE = auto()

### Models

class MunitionAllocation(OCCIDModel):
    munition_type: str
    qty: int = 0

class CombatTask(Task):
    combat_task: TaskCombat | None = None
    target_category: TargetCategory | None = None
    target_point: GlobalPosition | None = None
    munitions: list[MunitionAllocation]
    effect: str | None = None
    desired_bda: bool = False
