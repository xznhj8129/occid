"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class SensorErrorType(IntEnum):
    CEP = 0
    RMS = auto()

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

### Models

class Payload(OCCIDModel):
    'Object-carried sensor, effector, cargo, or other mounted payload'
    __occid_model_id__: ClassVar[int] = 179
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None

class SensorPayload(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 223
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: WeatherLimits
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: SensorFieldOfView | None = None
    zoom_range: NumericRange | None = None

class MeasurementQuality(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 136
    __occid_semantic_role__: ClassVar[str] = 'representation'
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: builtins.float | None = None
    bool: builtins.bool | None = None
    lat_err_m: builtins.float | None = None
    az_err_deg: builtins.float | None = None
    range_err_m: builtins.float | None = None

class ImageSensor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 106
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: WeatherLimits
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: SensorFieldOfView | None = None
    zoom_range: NumericRange | None = None
    fov: SensorFieldOfView | None = None
    night_vision: builtins.bool

class RFSensor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 200
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: WeatherLimits
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: SensorFieldOfView | None = None
    zoom_range: NumericRange | None = None
    frustum_shape: SensorFrustumShape | None = None
    freq_span: NumericRange | None = None
    chan_bw: builtins.float | None = None

class SensorFieldOfView(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 222
    __occid_semantic_role__: ClassVar[str] = 'representation'
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None
