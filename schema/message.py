"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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
    READ = auto()

class MessageType(IntEnum):
    BROADCAST = 0
    REQUEST = auto()
    REPLY = auto()

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

### Models

class ResponseMessage(OCCIDModel):
    'Message whose payload acknowledges, rejects, reports delivery, returns data, or reports errors'
    __occid_model_id__: ClassVar[int] = 211
    __occid_semantic_role__: ClassVar[str] = 'type'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: builtins.str | None = None

class MessageTarget(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 145
    __occid_semantic_role__: ClassVar[str] = 'representation'
    target_uid: UID

class DeliveryReceipt(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: builtins.str | None = None
    node_uid: UID
    delivery_state: DeliveryState
    seen_ts: builtins.float | None = None
    exec_ts: builtins.float | None = None
    error_code: builtins.str | None = None

class MessageTransferResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 146
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: MessageTarget
    dst: MessageTarget
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: builtins.str | None = None
    target_count: builtins.int = 0
    bytes_sent: builtins.int = 0
    delivery_state: DeliveryState | None = None
    error: builtins.str | None = None
