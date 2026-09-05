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
    __occid_model_id__: ClassVar[int] = 16
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('CommandAuthority', 'Lease')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: Semantic[UID]
    granted_by_uid: Semantic[UID] | None = None
    scope_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]

class CommandAuthority(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 36
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Authority'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: Semantic[UID]
    granted_by_uid: Semantic[UID] | None = None
    scope_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]
    organization_uid: Semantic[UID]
    role: Semantic[Role]

class Lease(OCCIDModel):
    'Bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 127
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Authority'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AttachmentLease', 'ControlLease')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: Semantic[UID]
    granted_by_uid: Semantic[UID] | None = None
    scope_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[UID]
    bound: Semantic[Condition]

class AttachmentLease(OCCIDModel):
    'Authority lease to an organization'
    __occid_model_id__: ClassVar[int] = 14
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Lease'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: Semantic[UID]
    granted_by_uid: Semantic[UID] | None = None
    scope_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[UID]
    bound: Semantic[Condition]
    parent_uid: Semantic[UID]
    attachment_uid: Semantic[UID]

class ControlLease(OCCIDModel):
    'Temporary direct control access'
    __occid_model_id__: ClassVar[int] = 47
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Lease'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Authority')]
    holder_uid: Semantic[UID]
    granted_by_uid: Semantic[UID] | None = None
    scope_uids: list[Semantic[UID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[UID]
    bound: Semantic[Condition]
    controller: Semantic[UID]
    control_level: ControlLevel
