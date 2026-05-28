"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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
    content_type: builtins.str | None = None
    text: builtins.str | None = None
    data: builtins.bytes | None = None

class CryptoKey(Protocol):
    key_id: StringID
    label: builtins.str | None = None
    crypto_type: CryptoType
    version: builtins.str | None = None
    fill_ts: builtins.float | None = None

class CryptoProfile(Protocol):
    active_crypto: CryptoType | None = None
    keyset_id: StringID | None = None
    keys: list[CryptoKey]

class LoRaProfile(Protocol):
    spreading_factor: builtins.int | None = None
    bandwidth_mhz: builtins.float | None = None
    coding_rate: builtins.str | None = None

class AprsProfile(Protocol):
    callsign: builtins.str | None = None
    path: builtins.str | None = None

class ElrsProfile(Protocol):
    packet_rate_hz: builtins.int | None = None
    telemetry_ratio: builtins.str | None = None

class FpvProfile(Protocol):
    video_standard: builtins.str | None = None
    low_latency: builtins.bool | None = None
