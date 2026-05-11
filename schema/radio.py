"""Generated from core/schemav2."""
from __future__ import annotations
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

class CryptoType(IntEnum):
    NONE = 0
    STATIC_KEY = auto()
    HOPSET = auto()
    STREAM = auto()
    PUBLIC_KEY = auto()

class RadioService(IntEnum):
    VOICE = 0
    APRS = auto()
    LORA = auto()
    RC_LINK = auto()
    TELEMETRY_LINK = auto()
    FPV_VIDEO = auto()
    MESHTASTIC = auto()
    MESHCORE = auto()

### Models

class FrequencyRange(OCCIDModel):
    low_mhz: float | None = None
    high_mhz: float | None = None
    center_mhz: float | None = None

class ChannelSpec(OCCIDModel):
    channel_id: str | None = None
    label: str | None = None
    frequency: FrequencyRange | None = None
    bandwidth_mhz: float | None = None
    spacing_mhz: float | None = None

class CryptoKey(OCCIDModel):
    key_id: str
    label: str | None = None
    crypto_type: CryptoType
    version: str | None = None
    fill_ts: float | None = None

class CryptoProfile(OCCIDModel):
    active_crypto: CryptoType | None = None
    keyset_id: str | None = None
    keys: list[CryptoKey] = Field(default_factory=list)

class LoRaProfile(OCCIDModel):
    spreading_factor: int | None = None
    bandwidth_mhz: float | None = None
    coding_rate: str | None = None

class AprsProfile(OCCIDModel):
    callsign: str | None = None
    path: str | None = None

class ElrsProfile(OCCIDModel):
    packet_rate_hz: int | None = None
    telemetry_ratio: str | None = None

class FpvProfile(OCCIDModel):
    video_standard: str | None = None
    low_latency: bool | None = None

class RadioProfile(OCCIDModel):
    service: RadioService | None = None
    bands: list[NATORadioBands] = Field(default_factory=list)
    waveform: Waveform | None = None
    frequency: FrequencyRange | None = None
    channel_plan: list[ChannelSpec] = Field(default_factory=list)
    active_channel_id: str | None = None
    crypto_types: list[CryptoType] = Field(default_factory=list)
    crypto_profile: CryptoProfile | None = None
    lora: LoRaProfile | None = None
    aprs: AprsProfile | None = None
    elrs: ElrsProfile | None = None
    fpv: FpvProfile | None = None

class EmitterNotationSchema(OCCIDModel):
    emitter_name: str | None = None
    emitter_class: str | None = None
    platform_class: str | None = None

class SignalMeasurement(OCCIDModel):
    value: float | None = None
    unit: str | None = None
    confidence: ConfidenceLevel | None = None

class LineOfBearingSchema(OCCIDModel):
    bearing_deg: float | None = None
    bearing_error_deg: float | None = None

class AngleOfArrivalSchema(OCCIDModel):
    azimuth_deg: float | None = None
    elevation_deg: float | None = None
    azimuth_error_deg: float | None = None
    elevation_error_deg: float | None = None

class PulseRepetitionIntervalSchema(OCCIDModel):
    pri_us: float | None = None
    jitter_us: float | None = None

class ScanCharacteristicsSchema(OCCIDModel):
    period_s: float | None = None
    frame_time_s: float | None = None

class SignalSchema(OCCIDModel):
    signal_id: str
    source_id: str | None = None
    emitter: EmitterNotationSchema | None = None
    frequency: FrequencyRange | None = None
    strength: SignalMeasurement | None = None
    line_of_bearing: LineOfBearingSchema | None = None
    angle_of_arrival: AngleOfArrivalSchema | None = None
    pulse_interval: PulseRepetitionIntervalSchema | None = None
    scan: ScanCharacteristicsSchema | None = None
    fixed_position_id: str | None = None
