"""Generated from core/schemav2."""
from __future__ import annotations
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
    C3 = 0
    I_S_R = auto()
    TELEMETRY = auto()
    RESPONSE = auto()

### Models

class Message(Communication):
    'Transmitted envelope plus payload'

class RetryProfile(OCCIDModel):
    max_attempts: int = 0
    base_delay_ms: int = 0
    backoff_factor: float = 1.0
    jitter_pct: float = 0.0

class RouteHint(OCCIDModel):
    next_hop: str | None = None
    hop_limit: int | None = None
    preferred_relays: list[NodeRef]
    avoid_nodes: list[NodeRef]

class MessageEnvelope(Message):
    msg_id: str
    msg_type: str
    src: str
    dst: str
    ts: float
    conversation_id: str | None = None
    ttl_s: float | None = None
    qos: QosTier = QosTier.ROUTINE
    priority: MessagePriority = MessagePriority.ROUTINE
    ack_mode: AckMode = AckMode.RECEIPT
    route_mode: RouteMode = RouteMode.DIRECT
    route_hint: RouteHint | None = None
    retry: RetryProfile | None = None

class MessageTarget(Message):
    target_id: str | None = None
    target_type: str | None = None
    callsign: str | None = None
    address: NetworkAddress | None = None
