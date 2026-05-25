"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class C3(Message):
    pass

class HumanTextMessage(C3):
    sender_id: str | None = None
    sender_name: str | None = None
    destination_id: str | None = None
    destination_group: str | None = None
    kind: str | None = None
    message: str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
