"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class CommandMessage(Message):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 136
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    command: SerializeAsAny[Command | StateChangeCommand | ProcessControlCommand | ConfigurationCommand | MotionCommand | ResourceCommand | ExecutionCommand]

class HumanTextMessage(Message):
    __occid_model_id__: ClassVar[int] = 137
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    message_id: builtins.str | None = None
    conversation_id: builtins.str | None = None
    reply_to_id: builtins.str | None = None
    sender_id: UID | None = None
    sender_name: builtins.str | None = None
    destination_id: UID | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
