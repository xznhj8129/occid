"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

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

### Models

class Sensor(State):
    pass

class MeasurementQuality(Sensor):
    lat_err_m: float | None = None
    az_err_deg: float | None = None
    range_err_m: float | None = None

class ImuSample(Sensor):
    acceleration: LocalVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    magnetic_field: LocalVector | None = None
    temperature_deg_c: float | None = None
    timestamp_us: int | None = None
    frame: BodyReferenceFrame | None = None

class TrackerState(Sensor):
    locked: bool | None = None
    target_id: str | None = None
    angular_error: LocalDirection | None = None
    search_box_size: int | None = None
    detections: VisionDetectionFrame | None = None
