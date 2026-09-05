"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class MilitaryRadioProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 165
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RadioProfile'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    name: builtins.str | None = None
    endpoint_uid: Semantic[UID] | None = None
    interface_name: builtins.str | None = None
    address: Semantic[NetworkAddress] | None = None
    radio_uid: Semantic[UID] | None = None
    link_type: LinkType | None = None
    net_type: NetType | None = None
    data_type: LinkDataType | None = None
    direction: LinkDirection | None = None
    rate_spec: Semantic[DataRateSpec] | None = None
    user_capacity: Semantic[LinkCapacity] | None = None
    network_uid: Semantic[UID] | None = None
    service: RadioService | None = None
    waveform: Waveform | None = None
    frequency: Semantic[FrequencyRange] | None = None
    channel_plan: list[Semantic[ChannelSpec]]
    active_channel_uid: Semantic[UID] | None = None
    crypto_types: list[CryptoType]
    crypto_profile: Semantic[CryptoProfile] | None = None
    lora: Semantic[LoRaProfile] | None = None
    aprs: Semantic[AprsProfile] | None = None
    elrs: Semantic[ElrsProfile] | None = None
    fpv: Semantic[FpvProfile] | None = None
    bands: list[NATORadioBands]
