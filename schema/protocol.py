"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class Protocol(OCCIDModel):
    'Wire format, message id space, payload format, command/result vocabulary, and mapping metadata'
    __occid_model_id__: ClassVar[int] = 194
    __occid_semantic_role__: ClassVar[str] = 'type'

class ProtocolPayload(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 196
    __occid_semantic_role__: ClassVar[str] = 'representation'
    format: ProtocolPayloadFormat
    content_type: builtins.str | None = None
    text: builtins.str | None = None
    data: builtins.bytes | None = None

class CryptoKey(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 44
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key_ref: builtins.str
    label: builtins.str | None = None
    crypto_type: CryptoType
    version: builtins.str | None = None
    fill_ts: builtins.float | None = None

class CryptoProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 45
    __occid_semantic_role__: ClassVar[str] = 'representation'
    active_crypto: CryptoType | None = None
    keyset_ref: builtins.str | None = None
    keys: list[CryptoKey]

class LoRaProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 124
    __occid_semantic_role__: ClassVar[str] = 'representation'
    spreading_factor: builtins.int | None = None
    bandwidth_mhz: builtins.float | None = None
    coding_rate: builtins.str | None = None

class AprsProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 11
    __occid_semantic_role__: ClassVar[str] = 'representation'
    callsign: builtins.str | None = None
    path: builtins.str | None = None

class ElrsProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 59
    __occid_semantic_role__: ClassVar[str] = 'representation'
    packet_rate_hz: builtins.int | None = None
    telemetry_ratio: builtins.str | None = None

class FpvProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 79
    __occid_semantic_role__: ClassVar[str] = 'representation'
    video_standard: builtins.str | None = None
    low_latency: builtins.bool | None = None
