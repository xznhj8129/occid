"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GUIDE = auto()
    FULL = auto()

### Models

class Authority(OCCIDModel):
    'Command, permission, delegation, authorization, or control-right context under which directed work may be assigned or exercised'
    __occid_model_id__: ClassVar[int] = 15
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[Constraint]

class ControlLease(OCCIDModel):
    'Time-bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 41
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[Constraint]
    asset_uid: UID
    control_level: ControlLevel
    lease_start: builtins.float
    lease_end: builtins.float
    lease_rev: builtins.int = 0
