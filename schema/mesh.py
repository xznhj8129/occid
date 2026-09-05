"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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

class MeshLink(OCCIDModel):
    'Observed state of a link between two mesh nodes'
    __occid_model_id__: ClassVar[int] = 150
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'LinkState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    link_uid: Semantic[UID] | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    signal: Semantic[SignalQuality] | None = None
    delivery: Semantic[DeliveryQuality] | None = None
    counters: Semantic[LinkCounters] | None = None
    src_uid: Semantic[UID]
    dst_uid: Semantic[UID]
    updated_ts: Semantic[Timestamp] | None = None

class MeshNode(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 151
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Node'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Node')]
    entity_uid: Semantic[UID] | None = None
    roles: list[CapabilityRole]
    addresses: list[Semantic[NetworkAddress]]
    links: dict[builtins.str, Semantic[Link]]
    radios: dict[builtins.str, Semantic[RadioProfile]]
    protocols: dict[builtins.str, Semantic[Protocol]]
    state: MeshNodeState | None = None
    last_seen_ts: Semantic[Timestamp] | None = None
    position: Semantic[GlobalPosition] | None = None
    link_state: Semantic[LinkState] | None = None

class MeshView(OCCIDModel):
    'Current observed mesh topology and node/link state'
    __occid_model_id__: ClassVar[int] = 154
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Network'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    epoch: builtins.int = 0
    nodes: list[Semantic[MeshNode]]
    links: list[Semantic[MeshLink]]

class MeshtasticMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 155
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    sender_node_num: builtins.int
    sender_name: builtins.str | None = None
    destination_node_num: builtins.int
    port: MeshtasticPort | None = None
    private_port_num: builtins.int | None = None
    text: builtins.str | None = None
    payload: builtins.bytes | None = None
    position: Semantic[MeshPositionSample] | None = None
    metrics: Semantic[MeshReceiveMetrics] | None = None

class MeshReceiveMetrics(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 153
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    state: Semantic[LinkState]

class MeshPositionSample(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 152
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    state: Semantic[LocationState]

class NodeHeartbeat(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 178
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TelemetryMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    node_uid: Semantic[UID]
    last_seen_ts: Semantic[Timestamp]
    node_state: MeshNodeState | None = None
    state: Semantic[LinkState]
