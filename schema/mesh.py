"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .link import LinkState
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

class MeshLink(LinkState):
    'Observed state of a link between two mesh nodes'
    __occid_model_id__: ClassVar[int] = 225
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    src_id: StringID
    dst_id: StringID
    updated_ts: builtins.float | None = None

class MeshNode(Node):
    __occid_model_id__: ClassVar[int] = 226
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    node_id: StringID
    state: MeshNodeState | None = None
    last_seen_ts: builtins.float | None = None
    position: GlobalPosition | None = None
    link_state: SerializeAsAny[LinkState | MeshLink] | None = None
    roles: list[CapabilityRole]

class MeshView(Network):
    'Current observed mesh topology and node/link state'
    __occid_model_id__: ClassVar[int] = 227
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    epoch: builtins.int = 0
    nodes: dict[builtins.str, MeshNode]
    links: list[MeshLink]
    partition_id: StringID | None = None

class MeshtasticMessage(Message):
    __occid_model_id__: ClassVar[int] = 228
    __occid_semantic_role__: ClassVar[str] = 'specialization'
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
    __occid_model_id__: ClassVar[int] = 229
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    state: SerializeAsAny[LinkState | MeshLink]

class MeshPositionSample(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 230
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    state: LocationState

class NodeHeartbeat(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 231
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    node_id: StringID
    last_seen_ts: builtins.float
    node_state: MeshNodeState | None = None
    state: SerializeAsAny[LinkState | MeshLink]
