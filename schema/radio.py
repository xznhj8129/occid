"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .link import Link

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

class Radio(Link):
    'What messages are transmitted over'
    __occid_model_id__: ClassVar[int] = 177

class FrequencyRange(Radio):
    __occid_model_id__: ClassVar[int] = 178
    low_mhz: builtins.float | None = None
    high_mhz: builtins.float | None = None
    center_mhz: builtins.float | None = None

class ChannelSpec(Radio):
    __occid_model_id__: ClassVar[int] = 179
    channel_id: StringID | None = None
    label: builtins.str | None = None
    frequency: FrequencyRange | None = None
    bandwidth_mhz: builtins.float | None = None
    spacing_mhz: builtins.float | None = None

class RadioProfile(Radio):
    __occid_model_id__: ClassVar[int] = 180
    service: RadioService | None = None
    waveform: Waveform | None = None
    frequency: FrequencyRange | None = None
    channel_plan: list[ChannelSpec]
    active_channel_id: StringID | None = None
    crypto_types: list[CryptoType]
    crypto_profile: CryptoProfile | None = None
    lora: LoRaProfile | None = None
    aprs: AprsProfile | None = None
    elrs: ElrsProfile | None = None
    fpv: FpvProfile | None = None
