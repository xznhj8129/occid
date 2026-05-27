"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class Telemetry(Message):
    "Communication about the sender's own internal state or process"

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

class NodeHeartbeat(Telemetry):
    node_id: str
    last_seen_ts: float
    node_state: MeshNodeState | None = None
    rssi: float | None = None
    snr: float | None = None
    hop_limit: int | None = None
    link_condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
