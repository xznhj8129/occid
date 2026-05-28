"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .feed import Link
from .message import Message
from .network import Network
from .node import Node
from .telemetry import TelemetryMessage

### Enums

class MeshNodeState(IntEnum):
    UNKNOWN = 0
    ACTIVE = auto()
    DEGRADED = auto()
    LOST = auto()

class MeshtasticPort(IntEnum):
    TEXT_MESSAGE = 0
    POSITION = auto()
    PRIVATE = auto()

### Models

class MeshLink(Link):
    src_id: str
    dst_id: str
    condition: LinkCondition
    connection_status: ConnectionStatus | None = None
    latency_ms: float | None = None
    packet_loss: float | None = None
    updated_ts: float | None = None

class MeshNode(Node):
    node_id: str
    state: MeshNodeState | None = None
    last_seen_ts: float | None = None
    position: GlobalPosition | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    roles: list[CapabilityRole]

class MeshView(Network):
    'Current observed mesh topology and node/link state'
    epoch: int = 0
    nodes: dict[str, MeshNode]
    links: list[MeshLink]
    partition_id: str | None = None

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

class MeshReceiveMetrics(TelemetryMessage):
    snr: float | None = None
    rssi: float | None = None
    hop_limit: int | None = None
    rx_time: float | None = None

class MeshPositionSample(TelemetryMessage):
    position: GlobalPosition
    position_ts: float | None = None
    pdop: float | None = None
    ground_speed: float | None = None
    ground_track: float | None = None
    sats_in_view: int | None = None

class NodeHeartbeat(TelemetryMessage):
    node_id: str
    last_seen_ts: float
    node_state: MeshNodeState | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
