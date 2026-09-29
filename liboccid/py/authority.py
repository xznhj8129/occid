"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GIDE = auto()
    FULL = auto()

### Models

class Authority(OCCIDModel):
    'Command, permission, delegation, authorization, or control-right context under which directed work may be assigned or exercised'
    __occid_model_id__: ClassVar[int] = 26
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('CommandAuthority', 'Lease')
    uid: Semantic[ID]
    holder_uid: Semantic[ID]
    granted_by_uid: Semantic[ID] | None = None
    scope_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]

class CommandAuthority(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Authority'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    holder_uid: Semantic[ID]
    granted_by_uid: Semantic[ID] | None = None
    scope_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]
    organization_uid: Semantic[ID]
    role: Semantic[Role]

class Lease(OCCIDModel):
    'Bounded control right issued under an Authority record'
    __occid_model_id__: ClassVar[int] = 164
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Authority'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AttachmentLease', 'ControlLease')
    uid: Semantic[ID]
    holder_uid: Semantic[ID]
    granted_by_uid: Semantic[ID] | None = None
    scope_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[ID]
    bound: Semantic[Condition]

class AttachmentLease(OCCIDModel):
    'Authority lease to an organization'
    __occid_model_id__: ClassVar[int] = 23
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Lease'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    holder_uid: Semantic[ID]
    granted_by_uid: Semantic[ID] | None = None
    scope_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[ID]
    bound: Semantic[Condition]
    parent_uid: Semantic[ID]
    attachment_uid: Semantic[ID]

class ControlLease(OCCIDModel):
    'Temporary direct control access'
    __occid_model_id__: ClassVar[int] = 63
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Lease'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    holder_uid: Semantic[ID]
    granted_by_uid: Semantic[ID] | None = None
    scope_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]
    asset_uid: Semantic[ID]
    bound: Semantic[Condition]
    controller: Semantic[ID]
    control_level: ControlLevel
