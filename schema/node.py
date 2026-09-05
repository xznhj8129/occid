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
    __occid_model_id__: ClassVar[int] = 177
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Communication'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeshNode',)
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Node')]
    entity_uid: Semantic[UID] | None = None
    roles: list[CapabilityRole]
    addresses: list[Semantic[NetworkAddress]]
    links: dict[builtins.str, Semantic[Link]]
    radios: dict[builtins.str, Semantic[RadioProfile]]
    protocols: dict[builtins.str, Semantic[Protocol]]
