"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import AckMode, Communication, MessagePriority, QosTier, RouteMode

### Enums

class MeshtasticPort(IntEnum):
    TEXT_MESSAGE = 0
    POSITION = auto()
    PRIVATE = auto()

class Message_type(IntEnum):
    C3 = 0
    I_S_R = auto()
    TELEMETRY = auto()
    RESPONSE = auto()

### Models

class Message(Communication):
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

class MessageTarget(Message):
    target_id: str | None = None
    target_type: str | None = None
    callsign: str | None = None
    address: NetworkAddress | None = None

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
