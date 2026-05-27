"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .transport import Transport

### Enums

class AddressKind(IntEnum):
    IPV4 = 0
    IPV6 = auto()
    MAC = auto()
    CALLSIGN = auto()
    URI = auto()

### Models

class Network(Transport):
    'Graph topology of information flow'

class RouteHint(Network):
    next_hop: str | None = None
    hop_limit: int | None = None
    preferred_relays: list[NodeRef]
    avoid_nodes: list[NodeRef]

class NetworkAddress(Network):
    kind: AddressKind
    value: str
    port: int | None = None

class MeshView(Network):
    epoch: int = 0
    nodes: dict[str, MeshNode]
    links: list[MeshLink]
    partition_id: str | None = None
