"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import Communication

### Enums

class MeshNodeState(IntEnum):
    UNKNOWN = 0
    ACTIVE = auto()
    DEGRADED = auto()
    LOST = auto()

### Models

class Node(Communication):
    pass

class NodeRef(Node):
    node_id: str

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
