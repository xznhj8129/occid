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
    'Time-indexed readings, readiness, calibration, and availability of an identified sensor'
    __occid_model_id__: ClassVar[int] = 336
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'SubjectState'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ImagingSensorState', 'TrackerState', 'FlightSensorConfiguration')
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]

class ImagingSensorState(OCCIDModel):
    'Current operating and pointing state of an imaging sensor'
    __occid_model_id__: ClassVar[int] = 168
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    run_state: SensorRunState
    mode: SensorMode | None = None
    gimbal_state: GimbalState | None = None
    gimbal_attitude: Semantic[EulerAngles] | None = None
    field_of_view: Semantic[SensorFieldOfView] | None = None

class TrackerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 390
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    locked: builtins.bool | None = None
    target_uid: Semantic[UID] | None = None
    angular_error: Semantic[LocalDirection] | None = None
    search_box_size: builtins.int | None = None
    detections: Semantic[VisionDetectionFrame] | None = None

class FlightSensorConfiguration(OCCIDModel):
    'Selected onboard flight/navigation sensor hardware as reported by a flight controller; native hardware names remain opaque identifiers'
    __occid_model_id__: ClassVar[int] = 125
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SensorState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    accelerometer: builtins.str | None = None
    barometer: builtins.str | None = None
    magnetometer: builtins.str | None = None
    airspeed: builtins.str | None = None
    rangefinder: builtins.str | None = None
    optical_flow: builtins.str | None = None
