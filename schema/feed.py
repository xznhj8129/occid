"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import Communication
from .root import SchemaKind

### Enums

class LinkCondition(IntEnum):
    UNKNOWN = 0
    GOOD = auto()
    DEGRADED = auto()
    INTERMITTENT = auto()
    LOST = auto()

class ConnectionStatus(IntEnum):
    UNKNOWN = 0
    ONLINE = auto()
    OFFLINE = auto()

class LinkDirection(IntEnum):
    RX = 0
    TX = auto()
    HALF_DUPLEX = auto()
    FULL_DUPLEX = auto()

class LinkDataType(IntEnum):
    TEXT = 0
    AUDIO = auto()
    VIDEO = auto()
    PACKET = auto()
    SERIAL = auto()
    CONTROL = auto()

class LinkType(IntEnum):
    BROADCAST = 0
    POINT_TO_POINT = auto()
    HUB = auto()
    MESH = auto()

class NetType(IntEnum):
    RF = 0
    CELLULAR = auto()
    LTE = auto()
    SATCOM = auto()
    WIFI = auto()
    WIRED = auto()

class Feed_type(IntEnum):
    LINK = 0
    STREAM = auto()

### Models

class Feed(Communication):
    'Information pipe'

class Link(Feed):
    'Discrete packet or message path with endpoints, addresses, capacity, condition, and status'

class Stream(Feed):
    'Continuous or ordered data flow such as telemetry, media, sensor samples, or raw bytes'

class BandwidthSpec(Link):
    mhz: float | None = None
    occupied_mhz: float | None = None
    usable_mhz: float | None = None

class DataRateSpec(Link):
    nominal_bps: float | None = None
    sustained_bps: float | None = None
    burst_bps: float | None = None

class LinkCapacity(Link):
    max_nodes: int | None = None
    max_users: int | None = None
    max_streams: int | None = None

class LinkEndpoint(Link):
    node_id: str | None = None
    interface_name: str | None = None
    address: NetworkAddress | None = None

class LinkSchema(Link):
    schema_id: str
    schema_type: SchemaKind = SchemaKind.LINK
    uuid: str | None = None
    name: str
    link_type: LinkType
    net_type: NetType
    io: int
    data_type: LinkDataType
    direction: LinkDirection | None = None
    bandwidth: BandwidthSpec | None = None
    rate_spec: DataRateSpec | None = None
    user_capacity: LinkCapacity | None = None
    network_id: str | None = None
    primary_address: NetworkAddress | None = None
    addresses: list[NetworkAddress] | None = None
    endpoints: list[LinkEndpoint]
    radio: RadioProfile | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
