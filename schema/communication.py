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

class ProtocolPayloadFormat(IntEnum):
    TEXT = 0
    XML = auto()
    JSON = auto()
    BYTES = auto()

### Models

class RetryProfile(OCCIDModel):
    max_attempts: int = 0
    base_delay_ms: int = 0
    backoff_factor: float = 1.0
    jitter_pct: float = 0.0

class NodeRef(OCCIDModel):
    node_id: str

class RouteHint(OCCIDModel):
    next_hop: str | None = None
    hop_limit: int | None = None
    preferred_relays: list[NodeRef]
    avoid_nodes: list[NodeRef]

class MessageEnvelope(OCCIDModel):
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

class DeliveryReceipt(OCCIDModel):
    msg_id: str
    node_id: str
    delivery_state: DeliveryState
    seen_ts: float | None = None
    exec_ts: float | None = None
    error_code: str | None = None

class CapabilityAdvert(OCCIDModel):
    node_id: str
    roles: list[CapabilityRole]
    link_ids: list[str]
    sensor_ids: list[str]
    payload_ids: list[str]

class StateDelta(OCCIDModel):
    entity_id: str
    changed_fields: list[str]
    source: str | None = None
    confidence: ConfidenceLevel | None = None

class MessageTarget(OCCIDModel):
    target_id: str | None = None
    target_type: str | None = None
    callsign: str | None = None
    address: NetworkAddress | None = None

class ProtocolPayload(OCCIDModel):
    format: ProtocolPayloadFormat
    content_type: str | None = None
    text: str | None = None
    data: bytes | None = None

class ProtocolEventMessage(OCCIDModel):
    uid: str
    event_type: str
    event_method: str | None = None
    callsign: str | None = None
    time_text: str | None = None
    start_text: str | None = None
    stale_text: str | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    detail: ProtocolPayload | None = None
    source_address: NetworkAddress | None = None
    targets: list[MessageTarget]

class HumanTextMessage(OCCIDModel):
    sender_id: str | None = None
    sender_name: str | None = None
    destination_id: str | None = None
    destination_group: str | None = None
    kind: str | None = None
    message: str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]

class MessageTransferResult(OCCIDModel):
    target_count: int = 0
    bytes_sent: int = 0
    delivery_state: DeliveryState | None = None
    error: str | None = None

class TransportCounters(OCCIDModel):
    rx_count: int = 0
    tx_count: int = 0
    parse_error_count: int = 0
    dropped_count: int = 0

class TransportError(OCCIDModel):
    error: str
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
