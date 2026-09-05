"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class Waveform(IntEnum):
    FM = 0
    AM = auto()
    OFDM = auto()
    USB = auto()
    LSB = auto()
    LORA = auto()
    LTE = auto()
    DSSS = auto()
    FHSS = auto()

class RadioService(IntEnum):
    VOICE = 0
    APRS = auto()
    LORA = auto()
    RC_LINK = auto()
    TELEMETRY_LINK = auto()
    FPV_VIDEO = auto()
    MESHTASTIC = auto()
    MESHCORE = auto()

class NATORadioBands(IntEnum):
    A_BAND_0_250M = 0
    B_BAND_250M_500M = auto()
    C_BAND_500M_1G = auto()
    D_BAND_1G_2G = auto()
    E_BAND_2G_3G = auto()
    F_BAND_3G_4G = auto()
    G_BAND_4G_6G = auto()
    H_BAND_6G_8G = auto()
    I_BAND_8G_10G = auto()
    J_BAND_10G_20G = auto()
    K_BAND_20G_40G = auto()
    L_BAND_40G_60G = auto()
    M_BAND_60G_100G = auto()

### Models

class Radio(OCCIDModel):
    'What messages are transmitted over'
    __occid_model_id__: ClassVar[int] = 214
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Link'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FrequencyRange', 'ChannelSpec', 'RadioProfile')
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

class FrequencyRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 91
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Radio'
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
    low_mhz: builtins.float | None = None
    high_mhz: builtins.float | None = None
    center_mhz: builtins.float | None = None

class ChannelSpec(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 30
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Radio'
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
    channel_uid: Semantic[UID] | None = None
    label: builtins.str | None = None
    frequency: Semantic[FrequencyRange] | None = None
    bandwidth_mhz: builtins.float | None = None
    spacing_mhz: builtins.float | None = None

class RadioProfile(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 215
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Radio'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryRadioProfile',)
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
