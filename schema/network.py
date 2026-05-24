"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .definition import SchemaKind

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

class AddressKind(IntEnum):
    IPV4 = 0
    IPV6 = auto()
    MAC = auto()
    CALLSIGN = auto()
    URI = auto()

### Models

class BandwidthSpec(OCCIDModel):
    mhz: float | None = None
    occupied_mhz: float | None = None
    usable_mhz: float | None = None

class DataRateSpec(OCCIDModel):
    nominal_bps: float | None = None
    sustained_bps: float | None = None
    burst_bps: float | None = None

class NetworkAddress(OCCIDModel):
    kind: AddressKind
    value: str
    port: int | None = None

class LinkCapacity(OCCIDModel):
    max_nodes: int | None = None
    max_users: int | None = None
    max_streams: int | None = None

class LinkEndpoint(OCCIDModel):
    node_id: str | None = None
    interface_name: str | None = None
    address: NetworkAddress | None = None

class LinkSchema(OCCIDModel):
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
    addresses: list[NetworkAddress]
    endpoints: list[LinkEndpoint]
    radio: RadioProfile | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
