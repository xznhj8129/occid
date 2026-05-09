"""Generated from core/schemav2."""
from __future__ import annotations
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

class SyncState(IntEnum):
    IN_SYNC = 0
    PARTIAL = auto()
    STALE = auto()
    DIVERGED = auto()

class NATOAlphabet(IntEnum):
    ALPHA = 0
    BRAVO = auto()
    CHARLIE = auto()
    DELTA = auto()
    ECHO = auto()
    FOXTROT = auto()
    GOLF = auto()
    HOTEL = auto()
    INDIA = auto()
    JULIETT = auto()
    KILO = auto()
    LIMA = auto()
    MIKE = auto()
    NOVEMBER = auto()
    OSCAR = auto()
    PAPA = auto()
    QUEBEC = auto()
    ROMEO = auto()
    SIERRA = auto()
    TANGO = auto()
    UNIFORM = auto()
    VICTOR = auto()
    WHISKEY = auto()
    XRAY = auto()
    YANKEE = auto()
    ZULU = auto()

class CapabilityRole(IntEnum):
    CONTROLLER = 0
    RELAY = auto()
    SENSOR = auto()
    EFFECTOR = auto()
    GATEWAY = auto()
    RECORDER = auto()

### Models

class RetryProfile(SigmaModel):
    max_attempts: int = '0'
    base_delay_ms: int = '0'
    backoff_factor: float = '1.0'
    jitter_pct: float = '0.0'

class NodeRef(SigmaModel):
    node_id: str

class RouteHint(SigmaModel):
    next_hop: str | None = None
    hop_limit: int | None = None
    preferred_relays: list[NodeRef] = Field(default_factory=list)
    avoid_nodes: list[NodeRef] = Field(default_factory=list)

class MessageEnvelope(SigmaModel):
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

class DeliveryReceipt(SigmaModel):
    msg_id: str
    node_id: str
    delivery_state: DeliveryState
    seen_ts: float | None = None
    exec_ts: float | None = None
    error_code: str | None = None

class CapabilityAdvert(SigmaModel):
    node_id: str
    roles: list[CapabilityRole] = Field(default_factory=list)
    link_ids: list[str] = Field(default_factory=list)
    sensor_ids: list[str] = Field(default_factory=list)
    payload_ids: list[str] = Field(default_factory=list)

class StateDelta(SigmaModel):
    entity_id: str
    changed_fields: list[str] = Field(default_factory=list)
    source: str | None = None
    confidence: ConfidenceLevel | None = None
