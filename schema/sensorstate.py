"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

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

class SensorState(State):
    'Onboard sensor readings, readiness, calibration, and availability'
    __occid_model_id__: ClassVar[int] = 190
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class TrackerState(SensorState):
    __occid_model_id__: ClassVar[int] = 191
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    locked: builtins.bool | None = None
    target_id: StringID | None = None
    angular_error: LocalDirection | None = None
    search_box_size: builtins.int | None = None
    detections: VisionDetectionFrame | None = None

class FlightSensorConfiguration(SensorState):
    'Selected onboard flight/navigation sensor hardware as reported by a flight controller; native hardware names remain opaque identifiers'
    __occid_model_id__: ClassVar[int] = 297
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    accelerometer: builtins.str | None = None
    barometer: builtins.str | None = None
    magnetometer: builtins.str | None = None
    airspeed: builtins.str | None = None
    rangefinder: builtins.str | None = None
    optical_flow: builtins.str | None = None
