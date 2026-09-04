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

class CommandAuthority(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 34
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    organization_uid: UID
    role: Role

class Lease(OCCIDModel):
    'Bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    asset_uid: UID
    bound: Predicate | BooleanLogic

class AttachmentLease(OCCIDModel):
    'Authority lease to an organization'
    __occid_model_id__: ClassVar[int] = 14
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    asset_uid: UID
    bound: Predicate | BooleanLogic
    parent_uid: UID
    attachment_uid: UID

class ControlLease(OCCIDModel):
    'Temporary direct control access'
    __occid_model_id__: ClassVar[int] = 42
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: UID
    granted_by_uid: UID | None = None
    scope_uids: list[UID]
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    asset_uid: UID
    bound: Predicate | BooleanLogic
    controller: UID
    control_level: ControlLevel
