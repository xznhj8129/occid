"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

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

class GimbalState(IntEnum):
    STOWED = 0
    STABILIZED = auto()
    SCANNING = auto()
    TRACKING = auto()

### Models

class SensorState(OCCIDModel):
    'Onboard sensor readings, readiness, calibration, and availability'
    __occid_model_id__: ClassVar[int] = 238
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TrackerState', 'FlightSensorConfiguration')

class TrackerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 274
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    locked: builtins.bool | None = None
    target_uid: Semantic[UID] | None = None
    angular_error: Semantic[LocalDirection] | None = None
    search_box_size: builtins.int | None = None
    detections: Semantic[VisionDetectionFrame] | None = None

class FlightSensorConfiguration(OCCIDModel):
    'Selected onboard flight/navigation sensor hardware as reported by a flight controller; native hardware names remain opaque identifiers'
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    accelerometer: builtins.str | None = None
    barometer: builtins.str | None = None
    magnetometer: builtins.str | None = None
    airspeed: builtins.str | None = None
    rangefinder: builtins.str | None = None
    optical_flow: builtins.str | None = None
