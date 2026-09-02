"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

### Models

class Link(OCCIDModel):
    'Communication capability or connection kind a node can use; mutable condition is reported separately as LinkState'
    __occid_model_id__: ClassVar[int] = 119
    __occid_semantic_role__: ClassVar[str] = 'type'
    schema_ref: builtins.str | None = None
    name: builtins.str | None = None
    endpoint_ref: builtins.str | None = None
    interface_name: builtins.str | None = None
    address: NetworkAddress | None = None
    radio_ref: builtins.str | None = None
    link_type: LinkType | None = None
    net_type: NetType | None = None
    data_type: LinkDataType | None = None
    direction: LinkDirection | None = None
    rate_spec: DataRateSpec | None = None
    user_capacity: LinkCapacity | None = None
    network_ref: builtins.str | None = None

class LinkState(OCCIDModel):
    'Time-varying condition and observed quality of a communication link'
    __occid_model_id__: ClassVar[int] = 122
    __occid_semantic_role__: ClassVar[str] = 'type'
    link_ref: builtins.str | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    signal: SignalQuality | None = None
    delivery: DeliveryQuality | None = None
    counters: LinkCounters | None = None

class DataRateSpec(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 47
    __occid_semantic_role__: ClassVar[str] = 'representation'
    nominal_bps: builtins.float | None = None
    sustained_bps: builtins.float | None = None
    burst_bps: builtins.float | None = None

class LinkCapacity(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'representation'
    max_nodes: builtins.int | None = None
    max_users: builtins.int | None = None
    max_streams: builtins.int | None = None

class SignalQuality(OCCIDModel):
    'Protocol-neutral observed receive-signal quality; values are present only when the source defines their physical or normalized meaning'
    __occid_model_id__: ClassVar[int] = 221
    __occid_semantic_role__: ClassVar[str] = 'representation'
    strength_dbm: builtins.float | None = None
    snr_db: builtins.float | None = None
    quality_ratio: builtins.float | None = None

class DeliveryQuality(OCCIDModel):
    'Protocol-neutral observed communication delivery quality over an observation interval'
    __occid_model_id__: ClassVar[int] = 49
    __occid_semantic_role__: ClassVar[str] = 'representation'
    latency_s: builtins.float | None = None
    packet_loss_ratio: builtins.float | None = None
    error_ratio: builtins.float | None = None

class LinkCounters(OCCIDModel):
    'Monotonic observed communication-link event counters'
    __occid_model_id__: ClassVar[int] = 121
    __occid_semantic_role__: ClassVar[str] = 'representation'
    error_count: builtins.int | None = None
    receive_error_count: builtins.int | None = None
    corrected_receive_count: builtins.int | None = None
