"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class MilitaryRadioProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 153
    __occid_semantic_role__: ClassVar[str] = 'representation'
    name: builtins.str | None = None
    endpoint_uid: UID | None = None
    interface_name: builtins.str | None = None
    address: NetworkAddress | None = None
    radio_uid: UID | None = None
    link_type: LinkType | None = None
    net_type: NetType | None = None
    data_type: LinkDataType | None = None
    direction: LinkDirection | None = None
    rate_spec: DataRateSpec | None = None
    user_capacity: LinkCapacity | None = None
    network_uid: UID | None = None
    service: RadioService | None = None
    waveform: Waveform | None = None
    frequency: FrequencyRange | None = None
    channel_plan: list[ChannelSpec]
    active_channel_uid: UID | None = None
    crypto_types: list[CryptoType]
    crypto_profile: CryptoProfile | None = None
    lora: LoRaProfile | None = None
    aprs: AprsProfile | None = None
    elrs: ElrsProfile | None = None
    fpv: FpvProfile | None = None
    bands: list[NATORadioBands]
