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

class TrackerState(SensorState):
    locked: builtins.bool | None = None
    target_id: StringID | None = None
    angular_error: LocalDirection | None = None
    search_box_size: builtins.int | None = None
    detections: VisionDetectionFrame | None = None
