"""Generated from core/schemav2."""
from __future__ import annotations
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

class DetectionBoxSpace(IntEnum):
    IMAGE_PIXEL = 0
    IMAGE_NORMALIZED = auto()
    BODY_ANGULAR = auto()
    WORLD = auto()

### Models

class SensorFieldOfView(OCCIDModel):
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None

class SpotterOrigin(OCCIDModel):
    position: GlobalPosition
    attitude: EulerAngles | None = None
    look_vector: LocalDirection | None = None

class MeasurementQuality(OCCIDModel):
    lat_err_m: float | None = None
    az_err_deg: float | None = None
    range_err_m: float | None = None

class ImuSample(OCCIDModel):
    acceleration: LocalVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    magnetic_field: LocalVector | None = None
    temperature_deg_c: float | None = None
    timestamp_us: int | None = None
    frame: BodyReferenceFrame | None = None

class VisionBox(OCCIDModel):
    space: DetectionBoxSpace
    bounds: BoundingBox

class VisionDetection(OCCIDModel):
    detection_id: str | None = None
    label: str | None = None
    class_id: int | None = None
    confidence: float | None = None
    box: VisionBox | None = None
    bearing: LocalDirection | None = None
    position: GlobalPosition | None = None
    source_frame_id: str | None = None
    attributes: list[MetadataEntry]

class VisionDetectionFrame(OCCIDModel):
    frame_id: str | None = None
    sensor_id: str | None = None
    timestamp_us: int | None = None
    detections: list[VisionDetection]

class TrackerState(OCCIDModel):
    locked: bool | None = None
    target_id: str | None = None
    angular_error: LocalDirection | None = None
    search_box_size: int | None = None
    detections: VisionDetectionFrame | None = None

class TrackerCommand(OCCIDModel):
    lock: bool | None = None
    reset: bool | None = None
    slew: LocalDirection | None = None
    search_box_size: int | None = None
    shutdown: bool | None = None

class SensorSchema(OCCIDModel):
    name: str
    model: str
    type: SensorType
    serial_uid: str = ''
    effect_domain: EffectDomain
    max_range: float
    ptz: bool
    spectrum: SensorSpectrum
    night_vision: bool
    all_weather: bool
    weather_limits: WeatherLimits
    error_margin: float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
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
