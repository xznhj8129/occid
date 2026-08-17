"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .communication import Communication
from .state import State
from .struct import Measurement

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

class Link(Communication):
    'Communication capability or connection kind a node can use; mutable condition is reported separately as LinkState'
    __occid_model_id__: ClassVar[int] = 71
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    schema_id: StringID | None = None
    name: builtins.str | None = None
    uuid: StringID | None = None
    endpoint_id: StringID | None = None
    interface_name: builtins.str | None = None
    address: NetworkAddress | None = None
    radio_id: builtins.str | None = None
    link_type: LinkType | None = None
    net_type: NetType | None = None
    data_type: LinkDataType | None = None
    direction: LinkDirection | None = None
    rate_spec: DataRateSpec | None = None
    user_capacity: LinkCapacity | None = None
    network_id: StringID | None = None

class DataRateSpec(Communication):
    __occid_model_id__: ClassVar[int] = 72
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    nominal_bps: builtins.float | None = None
    sustained_bps: builtins.float | None = None
    burst_bps: builtins.float | None = None

class LinkCapacity(Communication):
    __occid_model_id__: ClassVar[int] = 73
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    max_nodes: builtins.int | None = None
    max_users: builtins.int | None = None
    max_streams: builtins.int | None = None

class SignalQuality(Measurement):
    'Protocol-neutral observed receive-signal quality; values are present only when the source defines their physical or normalized meaning'
    __occid_model_id__: ClassVar[int] = 324
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    strength_dbm: builtins.float | None = None
    snr_db: builtins.float | None = None
    quality_ratio: builtins.float | None = None

class DeliveryQuality(Measurement):
    'Protocol-neutral observed communication delivery quality over an observation interval'
    __occid_model_id__: ClassVar[int] = 325
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    latency_s: builtins.float | None = None
    packet_loss_ratio: builtins.float | None = None
    error_ratio: builtins.float | None = None

class LinkCounters(Measurement):
    'Monotonic observed communication-link event counters'
    __occid_model_id__: ClassVar[int] = 326
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    error_count: builtins.int | None = None
    receive_error_count: builtins.int | None = None
    corrected_receive_count: builtins.int | None = None

class LinkState(State):
    'Time-varying condition and observed quality of a communication link'
    __occid_model_id__: ClassVar[int] = 327
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    link_id: StringID | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    signal: SignalQuality | None = None
    delivery: DeliveryQuality | None = None
    counters: LinkCounters | None = None
