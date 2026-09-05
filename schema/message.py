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

class Message(OCCIDModel):
    'Transmitted envelope plus payload'
    __occid_model_id__: ClassVar[int] = 156
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Communication'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeshtasticMessage', 'CommandMessage', 'HumanTextMessage', 'ObservationMessage', 'Delta', 'ResponseMessage', 'TelemetryMessage')
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int

class Delta(OCCIDModel):
    'K:V mapped delta of stored data to signal a change'
    __occid_model_id__: ClassVar[int] = 59
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    entity_uid: Semantic[UID]
    record: Semantic[UID]
    changed_fields: dict[builtins.str, Semantic[State]]
    updated_ts: Semantic[Timestamp]

class ResponseMessage(OCCIDModel):
    'Message whose payload acknowledges, rejects, reports delivery, returns data, or reports errors'
    __occid_model_id__: ClassVar[int] = 224
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DeliveryReceipt', 'MessageTransferResult')
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: Semantic[UID]

class DeliveryReceipt(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 58
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResponseMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: Semantic[UID]
    node_uid: Semantic[UID]
    delivery_state: DeliveryState
    seen_ts: Semantic[Timestamp] | None = None
    exec_ts: Semantic[Timestamp] | None = None
    error_code: builtins.str | None = None

class MessageTransferResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 157
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResponseMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    seq_reply: builtins.int | None = None
    response_to: Semantic[UID]
    target_count: builtins.int = 0
    bytes_sent: builtins.int = 0
    delivery_state: DeliveryState | None = None
    error: builtins.str | None = None
