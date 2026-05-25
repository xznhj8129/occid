"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import AckMode, Communication, MessagePriority, QosTier, RouteMode

### Enums

class MeshtasticPort(IntEnum):
    TEXT_MESSAGE = 0
    POSITION = auto()
    PRIVATE = auto()

class MessageType(IntEnum):
    C3 = 0
    I_S_R = auto()
    TELEMETRY = auto()
    RESPONSE = auto()

### Models

class Message(Communication):
    pass

class C3(Message):
    pass

class ISR(Message):
    pass

class Telemetry(Message):
    pass

class Response(Message):
    pass

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

class DeliveryReceipt(Response):
    msg_id: str
    node_id: str
    delivery_state: DeliveryState
    seen_ts: float | None = None
    exec_ts: float | None = None
    error_code: str | None = None

class CapabilityAdvert(Telemetry):
    node_id: str
    roles: list[CapabilityRole]
    link_ids: list[str]
    sensor_ids: list[str]
    payload_ids: list[str]

class StateDelta(Telemetry):
    entity_id: str
    changed_fields: list[str]
    source: str | None = None
    confidence: ConfidenceLevel | None = None

class MessageTarget(Message):
    target_id: str | None = None
    target_type: str | None = None
    callsign: str | None = None
    address: NetworkAddress | None = None

class ProtocolEventMessage(ISR):
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

class HumanTextMessage(C3):
    sender_id: str | None = None
    sender_name: str | None = None
    destination_id: str | None = None
    destination_group: str | None = None
    kind: str | None = None
    message: str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]

class MessageTransferResult(Response):
    target_count: int = 0
    bytes_sent: int = 0
    delivery_state: DeliveryState | None = None
    error: str | None = None

class TransportCounters(Telemetry):
    rx_count: int = 0
    tx_count: int = 0
    parse_error_count: int = 0
    dropped_count: int = 0

class TransportError(Telemetry):
    error: str
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None

class MeshReceiveMetrics(Telemetry):
    snr: float | None = None
    rssi: float | None = None
    hop_limit: int | None = None
    rx_time: float | None = None

class MeshPositionSample(Telemetry):
    position: GlobalPosition
    position_ts: float | None = None
    pdop: float | None = None
    ground_speed: float | None = None
    ground_track: float | None = None
    sats_in_view: int | None = None

class MeshtasticMessage(Message):
    sender_id: str
    sender_name: str | None = None
    destination_id: str
    port: MeshtasticPort | None = None
    private_port_num: int | None = None
    text: str | None = None
    payload: bytes | None = None
    position: MeshPositionSample | None = None
    metrics: MeshReceiveMetrics | None = None

class NodeHeartbeat(Telemetry):
    node_id: str
    last_seen_ts: float
    node_state: MeshNodeState | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
