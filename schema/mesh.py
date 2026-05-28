"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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
    src_id: StringID
    dst_id: StringID
    condition: LinkCondition
    connection_status: ConnectionStatus | None = None
    latency_ms: builtins.float | None = None
    packet_loss: builtins.float | None = None
    updated_ts: builtins.float | None = None

class MeshNode(Node):
    node_id: StringID
    state: MeshNodeState | None = None
    last_seen_ts: builtins.float | None = None
    position: GlobalPosition | None = None
    rssi: builtins.float | None = None
    snr: builtins.float | None = None
    hop_limit: builtins.int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    roles: list[CapabilityRole]

class MeshView(Network):
    'Current observed mesh topology and node/link state'
    epoch: builtins.int = 0
    nodes: dict[builtins.str, MeshNode]
    links: list[MeshLink]
    partition_id: StringID | None = None

class MeshtasticMessage(Message):
    sender_id: StringID
    sender_name: builtins.str | None = None
    destination_id: StringID
    port: MeshtasticPort | None = None
    private_port_num: builtins.int | None = None
    text: builtins.str | None = None
    payload: builtins.bytes | None = None
    position: MeshPositionSample | None = None
    metrics: MeshReceiveMetrics | None = None

class MeshReceiveMetrics(TelemetryMessage):
    snr: builtins.float | None = None
    rssi: builtins.float | None = None
    hop_limit: builtins.int | None = None
    rx_time: builtins.float | None = None

class MeshPositionSample(TelemetryMessage):
    position: GlobalPosition
    position_ts: builtins.float | None = None
    pdop: builtins.float | None = None
    ground_speed: builtins.float | None = None
    ground_track: builtins.float | None = None
    sats_in_view: builtins.int | None = None

class NodeHeartbeat(TelemetryMessage):
    node_id: StringID
    last_seen_ts: builtins.float
    node_state: MeshNodeState | None = None
    rssi: builtins.float | None = None
    snr: builtins.float | None = None
    hop_limit: builtins.int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
