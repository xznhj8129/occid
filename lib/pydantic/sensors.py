"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .aerial import WeatherLimits

### Enums

class SensorType(IntEnum):
    EO = 0
    EO_MULTISPECTRAL = auto()
    RADAR = auto()
    ELINT = auto()
    LIDAR = auto()

class SensorSpectrum(IntEnum):
    VISUAL = 0
    SWIR = auto()
    MWIR = auto()
    LWIR = auto()
    RF = auto()
    UV = auto()

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

class SensorErrorType(IntEnum):
    CEP = 0
    RMS = auto()

class SensorMode(IntEnum):
    OFF = 0
    LOOK = auto()
    SCAN = auto()
    TRACK = auto()

class SensorRunState(IntEnum):
    OFFLINE = 0
    READY = auto()
    ACTIVE = auto()
    DEGRADED = auto()

class SensorDataFormat(IntEnum):
    TEXT = 0
    STILL_IMAGE = auto()
    VIDEO = auto()
    TRACK = auto()
    RANGE = auto()
    POINT_CLOUD = auto()

class SensorAICapability(IntEnum):
    DETECTION = 0
    TRACKING = auto()
    CLASSIFICATION = auto()
    IDENTIFICATION = auto()
    OCR = auto()
    CHANGE_DETECTION = auto()

class SensorFrustumShape(IntEnum):
    CONICAL = 0
    RECTANGULAR = auto()
    ELLIPTICAL = auto()
    SECTOR = auto()

class GimbalState(IntEnum):
    STOWED = 0
    STABILIZED = auto()
    SCANNING = auto()
    TRACKING = auto()

### Models

class SensorFieldOfView(SigmaModel):
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None

class SpotterOrigin(SigmaModel):
    position: GlobalPosition
    attitude: EulerAngles | None = None
    look_vector: LocalDirection | None = None

class MeasurementQuality(SigmaModel):
    lat_err_m: float | None = None
    az_err_deg: float | None = None
    range_err_m: float | None = None

class SensorSchema(SigmaModel):
    name: str
    model: str
    type: SensorType
    serial_uid: str = '""'
    effect_domain: EffectDomain
    max_range: float
    ptz: bool
    spectrum: SensorSpectrum
    night_vision: bool
    all_weather: bool
    weather_limits: WeatherLimits = Field(default_factory=WeatherLimits)
    error_margin: float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat] = Field(default_factory=list)
    ai: list[SensorAICapability] = Field(default_factory=list)
    datalink: str
    field_of_view: SensorFieldOfView | None = None
    zoom_range: NumericRange | None = None
    run_state: SensorRunState | None = None
    mode: SensorMode | None = None
    sensor_family: str | None = None
    frustum_shape: SensorFrustumShape | None = None
    field_of_regard: SensorFieldOfView | None = None
    gimbal_state: GimbalState | None = None
    freq_span: NumericRange | None = None
    chan_bw: float | None = None
    emit_profile: str | None = None
    quality_hint: MeasurementQuality | None = None
