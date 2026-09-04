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
    __occid_model_id__: ClassVar[int] = 209
    __occid_semantic_role__: ClassVar[str] = 'type'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: UID

class Delta(OCCIDModel):
    'K:V mapped delta of stored data to signal a change'
    __occid_model_id__: ClassVar[int] = 52
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    entity_uid: UID
    record: UID
    changed_fields: dict[builtins.str, State]
    updated_ts: Timestamp

class DeliveryReceipt(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: UID
    node_uid: UID
    delivery_state: DeliveryState
    seen_ts: Timestamp | None = None
    exec_ts: Timestamp | None = None
    error_code: builtins.str | None = None

class MessageTransferResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 145
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: UID
    target_count: builtins.int = 0
    bytes_sent: builtins.int = 0
    delivery_state: DeliveryState | None = None
    error: builtins.str | None = None
