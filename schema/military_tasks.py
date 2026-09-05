"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class TaskCombat(IntEnum):
    DEFEND = 0
    ATTACK = auto()
    PROTECT = auto()
    COMBAT_SUPPORT = auto()
    COMBAT_RESERVE = auto()

### Models

class MunitionAllocation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 172
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    munition_type: builtins.str
    qty: builtins.int = 0

class CombatTaskProfile(OCCIDModel):
    'Military domain detail associated with a generic Task without creating a Task subtype'
    __occid_model_id__: ClassVar[int] = 34
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    task_uid: Semantic[UID]
    combat_task: TaskCombat | None = None
    target_category: TargetCategory | None = None
    target_point: Semantic[GlobalPosition] | None = None
    munitions: list[Semantic[MunitionAllocation]]
    effect: builtins.str | None = None
    desired_bda: builtins.bool = False
