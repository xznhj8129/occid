"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class CommandMessage(OCCIDModel):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 35
    __occid_semantic_role__: ClassVar[str] = 'type'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    command: StateChangeCommand | ProcessControlCommand | ConfigurationCommand | MotionCommand | ResourceCommand | ExecutionCommand

class HumanTextMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    message_ref: builtins.str | None = None
    conversation_ref: builtins.str | None = None
    reply_to_ref: builtins.str | None = None
    sender_uid: UID | None = None
    sender_name: builtins.str | None = None
    destination_uid: UID | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
