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
    __occid_model_id__: ClassVar[int] = 192
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Item'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SensorPayload', 'EffectsPayload')
    capabilities: list[Semantic[Capability]] | None = None

class SensorPayload(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 237
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Payload'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ImageSensor', 'RFSensor')
    capabilities: list[Semantic[Capability]] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: Semantic[WeatherLimits]
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: Semantic[SensorFieldOfView] | None = None
    zoom_range: Semantic[NumericRange] | None = None

class MeasurementQuality(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 147
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MetadataValue'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: Semantic[Timestamp]
    bool: builtins.bool | None = None
    lat_err_m: builtins.float | None = None
    az_err_deg: builtins.float | None = None
    range_err_m: builtins.float | None = None

class ImageSensor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 115
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorPayload'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: Semantic[WeatherLimits]
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: Semantic[SensorFieldOfView] | None = None
    zoom_range: Semantic[NumericRange] | None = None
    fov: Semantic[SensorFieldOfView] | None = None
    night_vision: builtins.bool

class RFSensor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 213
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorPayload'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_number: builtins.str | None = None
    effect_domain: EffectDomain
    max_range: builtins.float
    ptz: builtins.bool
    spectrum: SensorSpectrum
    all_weather: builtins.bool
    weather_limits: Semantic[WeatherLimits]
    error_margin: builtins.float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    field_of_view: Semantic[SensorFieldOfView] | None = None
    zoom_range: Semantic[NumericRange] | None = None
    frustum_shape: SensorFrustumShape | None = None
    freq_span: Semantic[NumericRange] | None = None
    chan_bw: builtins.float | None = None

class SensorFieldOfView(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 236
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    horizontal: Semantic[NumericRange] | None = None
    vertical: Semantic[NumericRange] | None = None
