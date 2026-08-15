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
    record: RecordMeta
    authority_id: StringID
    holder_id: StringID
    granted_by: StringID | None = None
    scope_refs: list[StringID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]

class ControlLease(Authority):
    'Time-bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 70
    asset_id: StringID
    control_level: ControlLevel
    lease_start: builtins.float
    lease_end: builtins.float
    lease_rev: builtins.int = 0
