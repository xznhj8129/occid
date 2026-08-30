"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Enums

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GUIDE = auto()
    FULL = auto()

### Models

class Authority(Control):
    'Command, permission, delegation, authorization, or control-right context under which directed work may be assigned or exercised'
    __occid_model_id__: ClassVar[int] = 302
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    uid: UID
    id: builtins.int
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]

class ControlLease(Authority):
    'Time-bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 70
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    asset_uid: UID
    control_level: ControlLevel
    lease_start: builtins.float
    lease_end: builtins.float
    lease_rev: builtins.int = 0
