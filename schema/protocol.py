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
    __occid_model_id__: ClassVar[int] = 210
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Communication'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ProtocolPayload', 'CryptoKey', 'CryptoProfile', 'LoRaProfile', 'AprsProfile', 'ElrsProfile', 'FpvProfile')

class ProtocolPayload(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 212
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    format: ProtocolPayloadFormat
    content_type: builtins.str | None = None
    text: builtins.str | None = None
    data: builtins.bytes | None = None

class CryptoKey(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 50
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key_ref: builtins.str
    label: builtins.str | None = None
    crypto_type: CryptoType
    version: builtins.str | None = None
    fill_ts: Semantic[Timestamp] | None = None

class CryptoProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    active_crypto: CryptoType | None = None
    keyset_uid: Semantic[UID] | None = None
    keys: list[Semantic[CryptoKey]]

class LoRaProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 135
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    spreading_factor: builtins.int | None = None
    bandwidth_mhz: builtins.float | None = None
    coding_rate: builtins.str | None = None

class AprsProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 11
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    callsign: builtins.str | None = None
    path: builtins.str | None = None

class ElrsProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 70
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    packet_rate_hz: builtins.int | None = None
    telemetry_ratio: builtins.str | None = None

class FpvProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 89
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Protocol'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    video_standard: builtins.str | None = None
    low_latency: builtins.bool | None = None
