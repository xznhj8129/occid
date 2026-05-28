"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .communication import Communication

### Enums

class DeliveryState(IntEnum):
    QUEUED = 0
    SENT = auto()
    RECEIVED = auto()
    ACKED = auto()
    NACKED = auto()
    EXECUTED = auto()
    EXPIRED = auto()
    DROPPED = auto()

class ReplyAck(IntEnum):
    ACK = 0
    RECEIVED = auto()
    WILCO = auto()

class AckMode(IntEnum):
    NONE = 0
    RECEIPT = auto()
    EXECUTION = auto()
    BOTH = auto()

class QosTier(IntEnum):
    BULK = 0
    ROUTINE = auto()
    URGENT = auto()
    CRITICAL = auto()

class MessagePriority(IntEnum):
    ROUTINE = 0
    PRIORITY = auto()
    IMMEDIATE = auto()
    FLASH = auto()

class RouteMode(IntEnum):
    DIRECT = 0
    RELAY = auto()
    STORE_FORWARD = auto()
    FLOOD = auto()

class ConflictPolicy(IntEnum):
    LAST_WRITE = 0
    AUTHORITY_WINS = auto()
    VECTOR_CLOCK = auto()
    MANUAL = auto()

class Message_type(IntEnum):
    COMMAND = 0
    TELEMETRY = auto()
    OBSERVATION = auto()
    RESPONSE = auto()

class ResponseMessage_type(IntEnum):
    DELIVERY_RECEIPT = 0
    MESSAGE_TRANSFER_RESULT = auto()

### Models

class Message(Communication):
    'Transmitted envelope plus payload'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int

class MessageTarget(OCCIDModel):
    target_id: StringID

class ResponseMessage(Message):
    'Message whose payload acknowledges, rejects, reports delivery, returns data, or reports errors'
    seq_reply: builtins.int

class DeliveryReceipt(ResponseMessage):
    node_id: StringID
    delivery_state: DeliveryState
    seen_ts: builtins.float | None = None
    exec_ts: builtins.float | None = None
    error_code: builtins.str | None = None

class MessageTransferResult(ResponseMessage):
    target_count: builtins.int = 0
    bytes_sent: builtins.int = 0
    delivery_state: DeliveryState | None = None
    error: builtins.str | None = None
