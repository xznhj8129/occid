"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class CapabilityRole(IntFlag):
    CONTROLLER = 1
    RELAY = auto()
    SENSOR = auto()
    EFFECTOR = auto()
    GATEWAY = auto()
    RECORDER = auto()

### Models

class Node(OCCIDModel):
    'Deployed compute and communications endpoint participating in OCCID on behalf of an Entity'
    __occid_model_id__: ClassVar[int] = 165
    __occid_semantic_role__: ClassVar[str] = 'type'
    uid: UID
    id: Annotated[IntID, IDNamespace('Node')]
    entity_uid: UID | None = None
    roles: list[CapabilityRole]
    addresses: list[NetworkAddress]
    links: dict[builtins.str, Link]
    radios: dict[builtins.str, RadioProfile]
    protocols: dict[builtins.str, Protocol]
