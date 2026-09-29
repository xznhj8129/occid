"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class CommandMessage(OCCIDModel):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 49
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[ID]
    dst: Semantic[ID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    command: Semantic[Command]

class HumanTextMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 147
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[ID]
    dst: Semantic[ID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    message_uid: Semantic[ID]
    conversation_uid: Semantic[ID]
    reply_to_uid: Semantic[ID]
    sender_uid: Semantic[ID]
    sender_name: builtins.str | None = None
    destination_uid: Semantic[ID]
    message: builtins.str
