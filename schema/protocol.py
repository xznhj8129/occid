"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .network import Transport

### Enums

class ProtocolPayloadFormat(IntEnum):
    TEXT = 0
    XML = auto()
    JSON = auto()
    BYTES = auto()

class CryptoType(IntEnum):
    NONE = 0
    STATIC_KEY = auto()
    HOPSET = auto()
    STREAM = auto()
    PUBLIC_KEY = auto()

### Models

class Protocol(Transport):
    'Wire format, message id space, payload format, command/result vocabulary, and mapping metadata'

class ProtocolPayload(Protocol):
    format: ProtocolPayloadFormat
    content_type: str | None = None
    text: str | None = None
    data: bytes | None = None

class CryptoKey(Protocol):
    key_id: str
    label: str | None = None
    crypto_type: CryptoType
    version: str | None = None
    fill_ts: float | None = None

class CryptoProfile(Protocol):
    active_crypto: CryptoType | None = None
    keyset_id: str | None = None
    keys: list[CryptoKey]

class LoRaProfile(Protocol):
    spreading_factor: int | None = None
    bandwidth_mhz: float | None = None
    coding_rate: str | None = None

class AprsProfile(Protocol):
    callsign: str | None = None
    path: str | None = None

class ElrsProfile(Protocol):
    packet_rate_hz: int | None = None
    telemetry_ratio: str | None = None

class FpvProfile(Protocol):
    video_standard: str | None = None
    low_latency: bool | None = None
