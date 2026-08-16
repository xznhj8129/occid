"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .attribute import Attribute
from .object import Item
from .property import MetadataValue

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

class Payload(Item):
    'Object-carried sensor, effector, cargo, or other mounted payload'
    __occid_model_id__: ClassVar[int] = 233
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class SensorPayload(Payload):
    __occid_model_id__: ClassVar[int] = 234
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    name: builtins.str
    model: builtins.str
    type: SensorType
    serial_uid: StringID
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

class MeasurementQuality(MetadataValue):
    __occid_model_id__: ClassVar[int] = 235
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    lat_err_m: builtins.float | None = None
    az_err_deg: builtins.float | None = None
    range_err_m: builtins.float | None = None

class ImageSensor(SensorPayload):
    __occid_model_id__: ClassVar[int] = 236
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    fov: SensorFieldOfView | None = None
    night_vision: builtins.bool

class RFSensor(SensorPayload):
    __occid_model_id__: ClassVar[int] = 237
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    frustum_shape: SensorFrustumShape | None = None
    freq_span: NumericRange | None = None
    chan_bw: builtins.float | None = None

class SensorFieldOfView(Attribute):
    __occid_model_id__: ClassVar[int] = 238
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None
