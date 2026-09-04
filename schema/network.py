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
    __occid_model_id__: ClassVar[int] = 164
    __occid_semantic_role__: ClassVar[str] = 'type'

class NetworkAddress(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 165
    __occid_semantic_role__: ClassVar[str] = 'representation'
    kind: AddressKind
    value: builtins.str
    port: builtins.int | None = None
