"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .communication import Communication

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

class Network(Communication):
    'Connectivity topology and routing state'
    __occid_model_id__: ClassVar[int] = 81
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class NetworkAddress(Network):
    __occid_model_id__: ClassVar[int] = 82
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    kind: AddressKind
    value: builtins.str
    port: builtins.int | None = None
