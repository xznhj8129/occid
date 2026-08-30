"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .communication import Communication

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

class Protocol(Communication):
    'Wire format, message id space, payload format, command/result vocabulary, and mapping metadata'
    __occid_model_id__: ClassVar[int] = 103
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class ProtocolPayload(Protocol):
    __occid_model_id__: ClassVar[int] = 104
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    format: ProtocolPayloadFormat
    content_type: builtins.str | None = None
    text: builtins.str | None = None
    data: builtins.bytes | None = None

class CryptoKey(Protocol):
    __occid_model_id__: ClassVar[int] = 105
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    key_ref: builtins.str
    label: builtins.str | None = None
    crypto_type: CryptoType
    version: builtins.str | None = None
    fill_ts: builtins.float | None = None

class CryptoProfile(Protocol):
    __occid_model_id__: ClassVar[int] = 106
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    active_crypto: CryptoType | None = None
    keyset_ref: builtins.str | None = None
    keys: list[CryptoKey]

class LoRaProfile(Protocol):
    __occid_model_id__: ClassVar[int] = 107
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    spreading_factor: builtins.int | None = None
    bandwidth_mhz: builtins.float | None = None
    coding_rate: builtins.str | None = None

class AprsProfile(Protocol):
    __occid_model_id__: ClassVar[int] = 108
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    callsign: builtins.str | None = None
    path: builtins.str | None = None

class ElrsProfile(Protocol):
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    packet_rate_hz: builtins.int | None = None
    telemetry_ratio: builtins.str | None = None

class FpvProfile(Protocol):
    __occid_model_id__: ClassVar[int] = 110
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    video_standard: builtins.str | None = None
    low_latency: builtins.bool | None = None
