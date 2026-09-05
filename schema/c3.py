"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class CommandMessage(OCCIDModel):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    command: Semantic[Command]

class HumanTextMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 111
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    message_uid: Semantic[UID] | None = None
    conversation_uid: Semantic[UID] | None = None
    reply_to_uid: Semantic[UID] | None = None
    sender_uid: Semantic[UID] | None = None
    sender_name: builtins.str | None = None
    destination_uid: Semantic[UID] | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: Semantic[GlobalPosition] | None = None
    targets: list[Semantic[UID]]
