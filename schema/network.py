"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class AddressKind(IntEnum):
    IPV4 = 0
    IPV6 = auto()
    MAC = auto()
    CALLSIGN = auto()
    URI = auto()

class NetworkError(IntEnum):
    PLACEHOLDER1 = 0
    PLACEHOLDER2 = auto()

### Models

class Network(OCCIDModel):
    'Connectivity topology and routing state'
    __occid_model_id__: ClassVar[int] = 175
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Communication'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeshView', 'NetworkAddress')

class NetworkAddress(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 176
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Network'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    kind: AddressKind
    value: builtins.str
    port: builtins.int | None = None
