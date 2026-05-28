"""Generated from core/schemav2."""
from __future__ import annotations
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

class Transport_type(IntEnum):
    NETWORK = 0
    CARRIER = auto()
    PROTOCOL = auto()

class Carrier_type(IntEnum):
    RADIO = 0

### Models

class Transport(Communication):
    'The form of information flow'

class Network(Transport):
    'Connectivity topology and routing state'

class NetworkAddress(Network):
    kind: AddressKind
    value: str
    port: int | None = None

class Carrier(Transport):
    'What messages are transmitted over'
