"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class Response(Message):
    'Message whose payload acknowledges, rejects, reports delivery, returns data, or reports errors'

class DeliveryReceipt(Response):
    msg_id: str
    node_id: str
    delivery_state: DeliveryState
    seen_ts: float | None = None
    exec_ts: float | None = None
    error_code: str | None = None

class MessageTransferResult(Response):
    target_count: int = 0
    bytes_sent: int = 0
    delivery_state: DeliveryState | None = None
    error: str | None = None
