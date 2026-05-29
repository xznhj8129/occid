"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .communication import Communication

### Enums

class CapabilityRole(IntFlag):
    CONTROLLER = 1
    RELAY = auto()
    SENSOR = auto()
    EFFECTOR = auto()
    GATEWAY = auto()
    RECORDER = auto()

### Models

class Node(Communication):
    'Communication identity of an entity, including addresses and available links'
    __occid_model_id__: ClassVar[int] = 83
    node_id: StringID
    entity_id: StringID | None = None
    roles: list[CapabilityRole]
    addresses: list[NetworkAddress]
    links: dict[builtins.str, SerializeAsAny[Link | MeshLink | Radio | FrequencyRange | ChannelSpec | RadioProfile]]
    radios: dict[builtins.str, RadioProfile]
    protocols: dict[builtins.str, SerializeAsAny[Protocol | ProtocolPayload | CryptoKey | CryptoProfile | LoRaProfile | AprsProfile | ElrsProfile | FpvProfile]]
