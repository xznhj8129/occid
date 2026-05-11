"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

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

class MeshReceiveMetrics(OCCIDModel):
    snr: float | None = None
    rssi: float | None = None
    hop_limit: int | None = None
    rx_time: float | None = None

class MeshPositionSample(OCCIDModel):
    position: GlobalPosition
    position_ts: float | None = None
    pdop: float | None = None
    ground_speed: float | None = None
    ground_track: float | None = None
    sats_in_view: int | None = None

class MeshtasticMessage(OCCIDModel):
    sender_id: str
    sender_name: str | None = None
    destination_id: str
    port: MeshtasticPort | None = None
    private_port_num: int | None = None
    text: str | None = None
    payload: bytes | None = None
    position: MeshPositionSample | None = None
    metrics: MeshReceiveMetrics | None = None

class MeshLink(OCCIDModel):
    src_id: str
    dst_id: str
    condition: LinkCondition
    connection_status: ConnectionStatus | None = None
    latency_ms: float | None = None
    packet_loss: float | None = None
    updated_ts: float | None = None

class NodeHeartbeat(OCCIDModel):
    node_id: str
    last_seen_ts: float
    node_state: MeshNodeState | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None

class MeshNode(OCCIDModel):
    node_id: str
    state: MeshNodeState | None = None
    last_seen_ts: float | None = None
    position: GlobalPosition | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    roles: list[CapabilityRole] = Field(default_factory=list)

class MeshView(OCCIDModel):
    epoch: int = '0'
    nodes: dict[str, MeshNode] = Field(default_factory=dict)
    links: list[MeshLink] = Field(default_factory=list)
    partition_id: str | None = None
