"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class CommandMessage(Message):
    'Message whose payload directs action'
    command: SerializeAsAny[Command | FlightCommand | TaskCommand | TrackerCommand]

class HumanTextMessage(Message):
    sender_id: StringID | None = None
    sender_name: builtins.str | None = None
    destination_id: StringID | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
