"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class TelemetryMessage(OCCIDModel):
    'Message whose payload reports sender or asset state'
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeshReceiveMetrics', 'MeshPositionSample', 'NodeHeartbeat', 'UAVTelemetryMessage', 'CapabilityAdvert', 'TransportCounters', 'TransportError')
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int

class UAVTelemetryMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 278
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    state: Semantic[EntityState]

class CapabilityAdvert(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 27
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    node_uid: Semantic[UID]
    roles: list[CapabilityRole]
    link_refs: list[builtins.str]
    sensor_refs: list[builtins.str]
    payload_refs: list[builtins.str]

class TransportCounters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 276
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    rx_count: builtins.int = 0
    tx_count: builtins.int = 0
    parse_error_count: builtins.int = 0
    dropped_count: builtins.int = 0

class TransportError(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 277
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    error: NetworkError
    source_address: Semantic[NetworkAddress] | None = None
    payload: Semantic[ProtocolPayload] | None = None
