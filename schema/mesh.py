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
    __occid_model_id__: ClassVar[int] = 139
    __occid_semantic_role__: ClassVar[str] = 'representation'
    link_uid: UID | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    signal: SignalQuality | None = None
    delivery: DeliveryQuality | None = None
    counters: LinkCounters | None = None
    src_uid: UID
    dst_uid: UID
    updated_ts: Timestamp | None = None

class MeshNode(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 140
    __occid_semantic_role__: ClassVar[str] = 'representation'
    uid: UID
    id: Annotated[IntID, IDNamespace('Node')]
    entity_uid: UID | None = None
    roles: list[CapabilityRole]
    addresses: list[NetworkAddress]
    links: dict[builtins.str, Link]
    radios: dict[builtins.str, RadioProfile]
    protocols: dict[builtins.str, Protocol]
    state: MeshNodeState | None = None
    last_seen_ts: Timestamp | None = None
    position: GlobalPosition | None = None
    link_state: LinkState | None = None

class MeshView(OCCIDModel):
    'Current observed mesh topology and node/link state'
    __occid_model_id__: ClassVar[int] = 143
    __occid_semantic_role__: ClassVar[str] = 'representation'
    epoch: builtins.int = 0
    nodes: list[MeshNode]
    links: list[MeshLink]

class MeshtasticMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 144
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    sender_node_num: builtins.int
    sender_name: builtins.str | None = None
    destination_node_num: builtins.int
    port: MeshtasticPort | None = None
    private_port_num: builtins.int | None = None
    text: builtins.str | None = None
    payload: builtins.bytes | None = None
    position: MeshPositionSample | None = None
    metrics: MeshReceiveMetrics | None = None

class MeshReceiveMetrics(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 142
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LinkState

class MeshPositionSample(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 141
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LocationState

class NodeHeartbeat(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 166
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    node_uid: UID
    last_seen_ts: Timestamp
    node_state: MeshNodeState | None = None
    state: LinkState
